from .backend import keras
from .backend import backend as K

__all__ = ['RNAdam']


class RNAdam(keras.optimizers.Optimizer):
    """RNAdam optimizer.
    # Arguments
        lr: float >= 0. Learning rate.
        beta_1: float, 0 < beta < 1. Generally close to 1.
        beta_2: float, 0 < beta < 1. Generally close to 1.
        epsilon: float >= 0. Fuzz factor. If `None`, defaults to `K.epsilon()`.
        schedule_decay: float, 0 < schedule_decay < 1.
        total_steps: int >= 0. Total number of training steps. Enable warmup by setting a positive value.
        warmup_proportion: 0 < warmup_proportion < 1. The proportion of increasing steps.
        min_lr: float >= 0. Minimum learning rate after warmup.
    """

    def __init__(self, lr=0.002, beta_1=0.9, beta_2=0.999,
                 epsilon=None, schedule_decay=0.004,
                 total_steps=0, warmup_proportion=0.1, min_lr=0. ,**kwargs):
        super(RNAdam, self).__init__(**kwargs)
        with K.name_scope(self.__class__.__name__):
            self.iterations = K.variable(0, dtype='int64', name='iterations')
            self.lr = K.variable(lr, name='lr')
            self.beta_1 = K.variable(beta_1, name='beta_1')
            self.beta_2 = K.variable(beta_2, name='beta_2')
            self.m_schedule = K.variable(1., name='m_schedule')
            self.total_steps = K.variable(total_steps, name='total_steps')
            self.warmup_proportion = K.variable(warmup_proportion, name='warmup_proportion')
            self.min_lr = K.variable(min_lr, name='min_lr')
        if epsilon is None:
            epsilon = K.epsilon()
        self.epsilon = epsilon
        self.schedule_decay = schedule_decay
        self.initial_total_steps = total_steps

    def get_updates(self, loss, params):
        grads = self.get_gradients(loss, params)
        self.updates = [K.update_add(self.iterations, 1)]

        t = K.cast(self.iterations, K.floatx()) + 1
        
        lr = self.lr
        
        if self.initial_total_steps > 0:
            warmup_steps = self.total_steps * self.warmup_proportion
            decay_steps = self.total_steps - warmup_steps
            lr = K.switch(
                t <= warmup_steps,
                lr * (t / warmup_steps),
                lr * (1.0 - K.minimum(t, decay_steps) / decay_steps),
            )

        ms = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='m_' + str(i)) for (i, p) in enumerate(params)]
        vs = [K.zeros(K.int_shape(p), dtype=K.dtype(p), name='v_' + str(i)) for (i, p) in enumerate(params)]

        self.weights = [self.iterations] + ms + vs

        beta_2_t = K.pow(self.beta_2, t)

        sma_inf = 2.0 / (1.0 - self.beta_2) - 1.0
        sma_t = sma_inf - 2.0 * t * beta_2_t / (1.0 - beta_2_t)

        momentum_cache_t = self.beta_1 * (1. - 0.5 * (K.pow(K.cast_to_floatx(0.96), t * self.schedule_decay)))
        momentum_cache_t_1 = self.beta_1 * (1. - 0.5 * (K.pow(K.cast_to_floatx(0.96), (t + 1) * self.schedule_decay)))
        m_schedule_new = self.m_schedule * momentum_cache_t
        m_schedule_next = self.m_schedule * momentum_cache_t * momentum_cache_t_1
        self.updates.append((self.m_schedule, m_schedule_new))

        for p, g, m, v in zip(params, grads, ms, vs):
            g_prime = g / (1. - m_schedule_new)
            m_t = (self.beta_1 * m) + (1. - self.beta_1) * g
            v_t = (self.beta_2 * v) + (1. - self.beta_2) * K.square(g)

            m_t_hat = m_t / (1. - m_schedule_next)
            v_t_hat = v_t / (1. - K.pow(self.beta_2, t))

            m_t_bar = (1. - momentum_cache_t) * g_prime + (momentum_cache_t_1 * m_t_hat)

            r_t = K.sqrt((sma_t - 4.0) / (sma_inf - 4.0) *
                         (sma_t - 2.0) / (sma_inf - 2.0) *
                         sma_inf / sma_t)

            p_t = K.switch(sma_t > 5, r_t * m_t_bar / (K.sqrt(v_t_hat + self.epsilon)), m_t_bar)

            p_t = p - self.lr * p_t

            self.updates.append(K.update(m, m_t))
            self.updates.append(K.update(v, v_t))
            new_p = p_t

            # Apply constraints.
            if getattr(p, 'constraint', None) is not None:
                new_p = p.constraint(new_p)

            self.updates.append(K.update(p, new_p))
        return self.updates

    def get_config(self):
        config = {
            'lr': float(K.get_value(self.lr)),
            'beta_1': float(K.get_value(self.beta_1)),
            'beta_2': float(K.get_value(self.beta_2)),
            'schedule_decay': self.schedule_decay,
            'epsilon': self.epsilon,
            'total_steps': float(K.get_value(self.total_steps)),
            'warmup_proportion': float(K.get_value(self.warmup_proportion)),
            'min_lr': float(K.get_value(self.min_lr)),
        }
        base_config = super(RNAdam, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
