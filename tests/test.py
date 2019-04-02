

def fact(n):
    if n==1:
        return 1
    return n*fact(n-1)


def solution(S):
    vowel = ['A','E','I','O','U']
    consonent={}
    vow={}
    for i in S:
        if i in vowel:
            vow[i] = 0
        else:
            consonent[i]=0

    for i in S:
        if i not in vowel:
            consonent[i]=consonent[i]+1
        else:
            vow[i]=vow[i]+1
    ckeys = len(consonent.keys())
    vkeys = len(vow.keys())
    ans=0
    if len(S)%2==0:
        if sum(consonent.values())!= sum(vow.values()):
            return ans
        else:
            ans = fact(ckeys) * fact(vkeys)
    else:
        if sum(consonent.values())<sum(vow.values()):
            return ans
        else:
            ans = fact(ckeys)*fact(vkeys)
    return ans

if __name__=="__main__":
    print(solution("AAAABCY"))


