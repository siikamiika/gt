import time
import ctypes

### https://github.com/soimort/translate-shell/issues/94#issuecomment-165433715
def RL(a, b):
    for c in range(0, len(b)-2, 3):
        d = b[c+2]
        d = ord(d) - 87 if d >= 'a' else int(d)
        xa = ctypes.c_uint32(a).value
        d = xa >> d if b[c+1] == '+' else xa << d
        a = a + d & 4294967295 if b[c] == '+' else a ^ d
    return ctypes.c_int32(a).value


def calc_tk(a):
    b = int(time.time() / 3600)
    d = a.encode('utf-8')
    a = b
    for di in d:
        a = RL(a + di, '+-a^+6')
    a = RL(a, '+-3^+b+-f')
    a = a if a >= 0 else ((a & 2147483647) + 2147483648)
    a %= pow(10, 6)
    return '%d.%d' % (a, a ^ b)
###
