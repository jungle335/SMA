class Environment:
    N = None
    t = None
    T = None

    def __init__(self, N, t, T):
        self.N = N
        self.t = t
        self.T = T

    def __str__(self):
        return f"Environment: N={self.N}, t={self.t}, T={self.T}"