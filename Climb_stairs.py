# You are climbing a staircase. It takes n steps to reach the top.

# Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?


#we solve this problem with dp, which means when we use the previous solutions in the next steps, so we dont re-calculate the steps for each stair
# and we think of it as from n --> 0 
def climbStairs(n: int) -> int:
    one, two = 1,1
    for i in range(n-1):
        temp = one + two
        two = one 
        one = temp
        
    return one
    

print(climbStairs(100))