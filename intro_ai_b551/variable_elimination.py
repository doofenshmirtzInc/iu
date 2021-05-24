import copy

# problem definition
states = ("rain", "sun")
trans = {"rain" : {"rain": 0.65, "sun": 0.35},
         "sun" : {"rain" : 0.25, "sun": 0.75}}
emission = {"rain": {"yes" : 0.6, "no" : 0.4},
            "sun" : {"yes": 0.2, "no": 0.8}}
initial = {"rain": 0.5, "sun": 0.5}
observed = ["yes", "yes", "no", "yes", "no", "no", "yes"]

M=2
N=len(observed)

###########################
# To compute P(S_M | W_0, W_1, ..., W_(N-1)), we first compute P(S_M, W_0, ...).
# Here's how to do this in the brute-force way.

joint = {"rain" : 0, "sun" : 0}
for s0 in states:
    for s1 in states:
        for s2 in states:
            for s3 in states:
                for s4 in states:
                    for s5 in states:
                        for s6 in states:
                            joint[s2] += initial[s0] * trans[s0][s1] * trans[s1][s2] * trans[s2][s3]*  trans[s3][s4] * trans[s4][s5] * trans[s5][s6] * \
                                emission[s0][observed[0]] * emission[s1][observed[1]] * emission[s2][observed[2]] * emission[s3][observed[3]] * \
                                emission[s4][observed[4]] * emission[s5][observed[5]] * emission[s6][observed[6]]

j_sum = joint["rain"] + joint["sun"]
print("Computed using brute force: " + str({ j:joint[j] / j_sum for j in joint}))

#############################
# obviously that's a big mess, and slow -- each every day requires another nested loop and 2x the computation time.
# so instead compute using variable elimination!

tau = {}

# First eliminate all variables before S_M -- e.g. S_0, S_1 ... S_(M-1)
for i in range(0, M):
    tau[i+1] = { s:0 for s in states }
    for s in states:
        for s2 in states:
            tau[i+1][s] += (tau[i][s2] if i > 0 else initial[s2]) * emission[s2][observed[i]] * trans[s2][s]

# Now eliminate all variables after S_M -- e.g. S_(M+1), ..., S_(N-1)
for i in range(N-1, M, -1):
    tau[i] = { s:0 for s in states }
    for s in states:
        for s2 in states:
            tau[i][s] += (tau[i+1][s2] if i+1 < N else 1) * emission[s2][observed[i]] * trans[s][s2]

# Now compute P(S_M | W_0, W_1, ...)
joint = {}
for s in states:
    joint[s] = tau[M][s] * tau[M+1][s] * emission[s][observed[M]]

    
j_sum = joint["rain"] + joint["sun"]
print("computed using Variable Elimination: " + str({ j:joint[j] / j_sum for j in joint}))


    
