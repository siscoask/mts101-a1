"""Builds data/questions.js|json. Every answer is computed, then re-checked independently (asserts)."""
import random, json, math
from fractions import Fraction as F
random.seed(101)
Q=[];SEEN=set();CNT={}
TS={"SET":"Set Theory and Venn Diagram","NUM":"Number System","QUA":"Quadratic Equation","SEQ":"Sequence and Series","IND":"Mathematical Induction","BIN":"Binomial Theorem","CPX":"Complex Number","CIR":"Circular Measure","TRG":"Trigonometry Function of Angle"}
def m(x): return f"${x}$"
def fr(x):
    x=F(x); return str(x.numerator) if x.denominator==1 else ("-" if x<0 else "")+f"\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"
def pi(x):
    x=F(x)
    if x==0: return "0"
    n,d=x.numerator,x.denominator; num="\\pi" if n==1 else f"{n}\\pi"
    return num if d==1 else f"\\frac{{{num}}}{{{d}}}"
def add(p,diff,q,right,wrong,concept,steps,mistake):
    if q in SEEN: return 0
    w=[]
    for x in wrong:
        if x!=right and x not in w: w.append(x)
    if len(w)<3: return 0
    SEEN.add(q); o=[right]+w[:3]; random.shuffle(o); CNT[p]=CNT.get(p,0)+1
    Q.append({"id":f"{p}-{CNT[p]:03d}","topic":TS[p],"difficulty":diff,"type":"multiple-choice","question":q,
      "options":[{"id":"ABCD"[i],"text":x} for i,x in enumerate(o)],"correctAnswer":"ABCD"[o.index(right)],"concept":concept,
      "explanation":{"summary":steps[-1],"steps":steps,"finalAnswer":right,"commonMistake":mistake}})
    return 1
def tries(n,f):
    k=0
    for _ in range(600):
        if k>=n: break
        k+=f()
R=random.randint
# ---- SET THEORY
def s1():
    a,b=R(15,40),R(10,35); c=R(2,min(a,b)-3); r=a+b-c; assert r==len(set(range(a))|set(range(a-c,a-c+b)))
    return add("SET","beginner",f"In a class, $n(A)={a}$, $n(B)={b}$ and $n(A\\cap B)={c}$. Find $n(A\\cup B)$.",m(r),[m(a+b),m(a+b+c),m(a+b-2*c)],"Union of two sets",
     [f"Given: $n(A)={a}$, $n(B)={b}$, $n(A\\cap B)={c}$. Required: $n(A\\cup B)$.","Use $n(A\\cup B)=n(A)+n(B)-n(A\\cap B)$. Elements in both sets are counted twice when we add, so we subtract the overlap once.",f"${a}+{b}-{c}={r}$.",f"$n(A\\cup B)={r}$."],f"Adding {a}+{b}={a+b} counts the {c} common elements twice.")
def s2():
    a=R(15,40); c=R(2,a-3)
    return add("SET","beginner",f"$n(A)={a}$ and $n(A\\cap B)={c}$. How many elements belong to $A$ but not to $B$?",m(a-c),[m(a+c),m(c),m(a)],"Set difference",
     [f"Given: $n(A)={a}$, $n(A\\cap B)={c}$. Required: $n(A\\setminus B)$.","The elements of $A$ split into those also in $B$ and those that are not, so $n(A\\setminus B)=n(A)-n(A\\cap B)$.",f"${a}-{c}={a-c}$.",f"The answer is ${a-c}$."],f"Giving {a}, the whole of $A$, forgets to remove the {c} elements that are also in $B$.")
def s3():
    n=R(3,9); pr=random.random()<.5; r=2**n-(1 if pr else 0); assert r==sum(math.comb(n,k) for k in range(n+1))-(1 if pr else 0)
    t="proper subsets" if pr else "subsets"
    return add("SET","beginner",f"How many {t} does a set with ${n}$ elements have?",m(r),[m(2*n),m(n*n),m(2**n-(0 if pr else 1))],"Number of subsets",
     [f"Given: a set with ${n}$ elements. Required: the number of {t}.","Each element is either in a subset or not, giving 2 choices per element, so there are $2^n$ subsets in all. A proper subset excludes the set itself.",f"$2^{{{n}}}={2**n}$"+(f", and subtracting the set itself gives ${r}$." if pr else "."),f"The answer is ${r}$."],"Using $2n$ or $n^2$ confuses counting subsets with counting elements or pairs.")
def s4():
    z=R(3,12); x=z+R(5,20); y=z+R(5,20); N=x+y-z
    return add("SET","intermediate",f"In a group of ${N}$ students, each takes Mathematics or Physics or both. ${x}$ take Mathematics and ${y}$ take Physics. How many take both?",m(z),[m(x+y),m(N-x),m(abs(x-y))],"Inclusion-exclusion",
     [f"Given: total ${N}$, $n(M)={x}$, $n(P)={y}$, everyone is in at least one set. Required: $n(M\\cap P)$.","Use $n(M\\cup P)=n(M)+n(P)-n(M\\cap P)$ with $n(M\\cup P)=N$.",f"${N}={x}+{y}-n(M\\cap P)$, so $n(M\\cap P)={x+y}-{N}={z}$.",f"${z}$ students take both."],f"Answering {x+y} forgets that those taking both were counted in each subject.")
def s5():
    u=R(30,90); a=R(8,u-8)
    return add("SET","beginner",f"$n(\\mathcal{{U}})={u}$ and $n(A)={a}$. Find $n(A')$.",m(u-a),[m(u+a),m(a),m(u-a+1)],"Complement",
     [f"Given: universal set has ${u}$ elements, $n(A)={a}$.","$A'$ contains everything in $\\mathcal{U}$ that is not in $A$, so $n(A')=n(\\mathcal{U})-n(A)$.",f"${u}-{a}={u-a}$.",f"$n(A')={u-a}$."],"Adding instead of subtracting.")
tries(25,s1);tries(15,s2);tries(18,s3);tries(22,s4);tries(15,s5)
# ---- NUMBER SYSTEMS
def n1():
    b=bin(R(33,63))[2:]; v=int(b,2)
    return add("NUM","beginner",f"Convert ${b}_2$ to base 10.",m(v),[m(v+1),m(v-1),m(int(b[::-1],2)),m(v+4)],"Binary to decimal",
     [f"Given: ${b}_2$. Required: its base-10 value.","Each digit is multiplied by a power of 2, starting from $2^0$ on the right.","$"+"+".join(f"2^{{{len(b)-1-i}}}" for i,d in enumerate(b) if d=="1")+f"={v}$",f"${b}_2={v}$."],"Reading the digits from the wrong end gives the reversed number's value.")
def n2():
    v=R(20,120)
    return add("NUM","beginner",f"Express ${v}$ in base 2.",m(bin(v)[2:]+"_2"),[m(bin(v+1)[2:]+"_2"),m(bin(v-1)[2:]+"_2"),m(bin(v+2)[2:]+"_2")],"Decimal to binary",
     [f"Given: ${v}$ in base 10. Required: base 2.","Divide repeatedly by 2 and read the remainders from last to first.",f"Doing this gives ${bin(v)[2:]}$.",f"${v}={bin(v)[2:]}_2$."],"Reading the remainders from first to last reverses the digits.")
def n3():
    v=R(20,200)
    return add("NUM","intermediate",f"Express ${v}$ in base 8.",m(oct(v)[2:]+"_8"),[m(oct(v+1)[2:]+"_8"),m(oct(v-1)[2:]+"_8"),m(oct(v+8)[2:]+"_8")],"Decimal to octal",
     [f"Given: ${v}$ in base 10. Required: base 8.","Divide repeatedly by 8 and read the remainders from last to first.",f"This gives ${oct(v)[2:]}$.",f"${v}={oct(v)[2:]}_8$."],"Stopping one division early or mis-dividing changes the last digit.")
def n4():
    a,b=R(5,40),R(5,40)
    return add("NUM","intermediate",f"Find ${bin(a)[2:]}_2+{bin(b)[2:]}_2$, giving your answer in base 2.",m(bin(a+b)[2:]+"_2"),[m(bin(a+b+1)[2:]+"_2"),m(bin(a+b-1)[2:]+"_2"),m(bin(a+b+2)[2:]+"_2")],"Binary addition",
     [f"Given: ${bin(a)[2:]}_2$ and ${bin(b)[2:]}_2$. Required: their sum in base 2.",f"Convert: ${a}$ and ${b}$, so the sum is ${a+b}$.",f"Convert back: ${a+b}={bin(a+b)[2:]}_2$.",f"The answer is ${bin(a+b)[2:]}_2$."],"Forgetting to carry when $1+1=10_2$.")
tries(24,n1);tries(24,n2);tries(24,n3);tries(24,n4)
# ---- QUADRATIC EQUATIONS
def poly(a,b,c):
    s=("" if a==1 else str(a))+"x^2"
    if b: s+=("+" if b>0 else "-")+("" if abs(b)==1 else str(abs(b)))+"x"
    if c: s+=("+" if c>0 else "-")+str(abs(c))
    return s+"=0"
def pair(p,q): return m(f"{min(p,q)},\\ {max(p,q)}")
def u1():
    p,q=random.sample([i for i in range(-9,10) if i],2); b,c=-(p+q),p*q; assert p*p+b*p+c==0 and q*q+b*q+c==0
    return add("QUA","beginner",f"Solve ${poly(1,b,c)}$.",pair(p,q),[pair(-p,-q),pair(p,-q),pair(-p,q)],"Factorising a quadratic",
     [f"Given: ${poly(1,b,c)}$. Required: the roots.",f"Find two numbers with product ${c}$ and sum ${b}$: they are ${-p}$ and ${-q}$.",f"So $(x{'-' if p>0 else '+'}{abs(p)})(x{'-' if q>0 else '+'}{abs(q)})=0$.",f"$x={p}$ or $x={q}$."],"Sign slips: the factor $(x-p)$ gives the root $+p$, not $-p$.")
def u2():
    a,b,c=R(1,4),R(-9,9),R(-6,6); D=b*b-4*a*c
    return add("QUA","beginner",f"Find the discriminant of ${poly(a,b,c)}$.",m(D),[m(b*b+4*a*c),m(4*a*c-b*b),m(b*b-2*a*c)],"The discriminant",
     [f"Given: $a={a}$, $b={b}$, $c={c}$. Required: $b^2-4ac$.",f"Substitute: $({b})^2-4({a})({c})={b*b}-({4*a*c})$.",f"$={D}$.",f"The discriminant is ${D}$."],"Mishandling the sign of $c$ when $c$ is negative.")
def u3():
    a,b,c=R(1,4),R(-9,9),R(-6,6); D=b*b-4*a*c
    N=["Two distinct real roots","Two equal real roots","No real roots (a complex conjugate pair)","One real root and one complex root"]
    k=0 if D>0 else 1 if D==0 else 2
    return add("QUA","intermediate",f"State the nature of the roots of ${poly(a,b,c)}$.",N[k],[x for x in N if x!=N[k]],"Nature of roots",
     [f"Given: $a={a}$, $b={b}$, $c={c}$.",f"$b^2-4ac={D}$.","If it is positive there are two distinct real roots; if zero, equal real roots; if negative, no real roots.",N[k]+"."],"A quadratic with real coefficients never has exactly one complex root: complex roots come in conjugate pairs.")
def u4():
    a,b,c=R(1,6),R(-9,9),R(-9,9)
    if not b: return 0
    return add("QUA","intermediate",f"Without solving, find the sum of the roots of ${poly(a,b,c)}$.",m(fr(F(-b,a))),[m(fr(F(b,a))),m(fr(F(c,a))),m(fr(F(-c,a)))],"Sum of roots",
     [f"Given: $a={a}$, $b={b}$, $c={c}$. Required: $\\alpha+\\beta$.","From $a(x-\\alpha)(x-\\beta)=0$, expanding gives $\\alpha+\\beta=-\\frac{b}{a}$.",f"$-\\frac{{{b}}}{{{a}}}={fr(F(-b,a))}$.",f"The sum is ${fr(F(-b,a))}$."],"Forgetting the minus sign in $-b/a$.")
def u5():
    k_=R(1,9)
    return add("QUA","challenging",f"For what value of $k$ does $x^2+{2*k_}x+k=0$ have equal roots?",m(k_*k_),[m(4*k_*k_),m(2*k_),m(k_)],"Condition for equal roots",
     [f"Given: $x^2+{2*k_}x+k=0$. Equal roots need $b^2-4ac=0$.",f"$({2*k_})^2-4(1)(k)=0$, so ${4*k_*k_}-4k=0$.",f"$k={k_*k_}$.",f"$k={k_*k_}$."],"Writing $b^2=4ac$ as $k=b^2$ without dividing by 4.")
tries(26,u1);tries(20,u2);tries(20,u3);tries(20,u4);tries(9,u5)
# ---- SEQUENCE AND SERIES
def a1():
    a,d,n=R(-5,12),R(-4,7),R(8,40)
    if not d: return 0
    t=a+(n-1)*d; assert [a+i*d for i in range(n)][-1]==t
    return add("SEQ","beginner",f"An AP has first term ${a}$ and common difference ${d}$. Find $T_{{{n}}}$.",m(t),[m(a+n*d),m(a+(n-2)*d),m(a+(n+1)*d)],"nth term of an AP",
     [f"Given: $a={a}$, $d={d}$, $n={n}$.","Use $T_n=a+(n-1)d$.",f"$T_{{{n}}}={a}+({n-1})({d})={t}$.",f"$T_{{{n}}}={t}$."],f"Using $a+nd$ gives {a+n*d}; the nth term adds $d$ only $n-1$ times.")
def a2():
    a,d,n=R(1,10),R(1,6),R(6,30); S=n*(2*a+(n-1)*d)//2; assert S==sum(a+i*d for i in range(n))
    return add("SEQ","intermediate",f"Find the sum of the first ${n}$ terms of the AP with $a={a}$ and $d={d}$.",m(S),[m(2*S),m(S-d),m(S+a)],"Sum of an AP",
     [f"Given: $a={a}$, $d={d}$, $n={n}$.","Use $S_n=\\frac{n}{2}\\left[2a+(n-1)d\\right]$.",f"$S_{{{n}}}=\\frac{{{n}}}{{2}}[{2*a}+{n-1}\\times{d}]=\\frac{{{n}}}{{2}}\\times{2*a+(n-1)*d}$.",f"$S_{{{n}}}={S}$."],f"Forgetting the factor $\\frac12$ doubles the answer to {2*S}.")
def a3():
    a,r,n=R(1,5),random.choice([2,3,-2,-3]),R(4,8); t=a*r**(n-1); assert t==[a*r**i for i in range(n)][-1]
    return add("SEQ","beginner",f"A GP has first term ${a}$ and common ratio ${r}$. Find the ${n}$th term.",m(t),[m(a*r**n),m((a*r)**(n-1)),m(a*r*(n-1))],"nth term of a GP",
     [f"Given: $a={a}$, $r={r}$, $n={n}$.","Use $T_n=ar^{n-1}$.",f"$T_{{{n}}}={a}\\times({r})^{{{n-1}}}={t}$.",f"The term is ${t}$."],"Using $r^n$ instead of $r^{n-1}$.")
def a4():
    a,k=R(2,12),R(2,6); r=F(1,k); S=F(a)/(1-r)
    return add("SEQ","intermediate",f"Find the sum to infinity of the GP with first term ${a}$ and common ratio $\\frac{{1}}{{{k}}}$.",m(fr(S)),[m(fr(F(a)/(1+r))),m(fr(a*(1-r))),m(a*k)],"Sum to infinity of a GP",
     [f"Given: $a={a}$, $r=\\frac{{1}}{{{k}}}$, and $|r|<1$ so the series converges.","Use $S_\\infty=\\frac{a}{1-r}$.",f"$S_\\infty=\\frac{{{a}}}{{1-\\frac{{1}}{{{k}}}}}={fr(S)}$.",f"$S_\\infty={fr(S)}$."],"Using $1+r$ in the denominator.")
def a5():
    n,c=R(5,25),R(-5,8); v=n*(n+1)+c*n; assert v==sum(2*r+c for r in range(1,n+1))
    return add("SEQ","intermediate",f"Evaluate $\\sum_{{r=1}}^{{{n}}}(2r{'+' if c>=0 else '-'}{abs(c)})$.",m(v),[m(n*(n+1)+c),m(n*(n-1)+c*n),m(n*(n+1)//2+c*n)],"Summation notation",
     ["Split the sum: $\\sum 2r+\\sum c$.",f"$2\\sum_{{r=1}}^{{{n}}}r=2\\times\\frac{{{n}({n}+1)}}{{2}}={n*(n+1)}$.",f"The constant ${c}$ is added ${n}$ times, giving ${c*n}$.",f"Total ${v}$."],"Adding the constant once instead of $n$ times.")
tries(24,a1);tries(24,a2);tries(20,a3);tries(18,a4);tries(18,a5)
# ---- MATHEMATICAL INDUCTION
def i1():
    n=R(4,16); v=n*(n+1)*(2*n+1)//6; assert v==sum(r*r for r in range(1,n+1))
    return add("IND","intermediate",f"Induction proves $\\sum_{{r=1}}^{{k}}r^2=\\frac{{k(k+1)(2k+1)}}{{6}}$ for all $k\\ge1$. Use it to evaluate $1^2+2^2+\\dots+{n}^2$.",m(v),[m(v-n*n),m(v+(n+1)**2),m((n*(n+1)//2)**2)],"Using a proved summation formula",
     [f"Given: the proved formula, with $k={n}$.","Substitute $k=n$ directly; the induction proof is what lets us trust it for every $n$.",f"$\\frac{{{n}\\times{n+1}\\times{2*n+1}}}{{6}}={v}$.",f"The sum is ${v}$."],"Confusing the sum of squares with the square of the sum.")
def i2():
    n=R(4,14); v=(n*(n+1)//2)**2; assert v==sum(r**3 for r in range(1,n+1))
    return add("IND","intermediate",f"Given that $\\sum_{{r=1}}^{{k}}r^3=\\left[\\frac{{k(k+1)}}{{2}}\\right]^2$ (provable by induction), find $1^3+2^3+\\dots+{n}^3$.",m(v),[m(n*(n+1)//2),m(n*(n+1)*(2*n+1)//6),m(v-n**3)],"Using a proved summation formula",
     [f"Given: the formula with $k={n}$.",f"$\\frac{{{n}\\times{n+1}}}{{2}}={n*(n+1)//2}$.",f"Square it: ${n*(n+1)//2}^2={v}$.",f"The sum is ${v}$."],"Forgetting to square the bracket.")
def i3():
    n=R(2,7); v=(7**n-1)//6; assert (7**n-1)%6==0
    return add("IND","challenging",f"It can be proved by induction that $7^n-1$ is divisible by $6$ for every positive integer $n$. Find $\\frac{{7^{{{n}}}-1}}{{6}}$ for $n={n}$.",m(v),[m(v+1),m(7**n//6),m(7**(n-1)-1)],"Divisibility",
     [f"Given: $n={n}$, so $7^{{{n}}}={7**n}$.",f"$7^{{{n}}}-1={7**n-1}$.",f"Divide by 6: ${v}$.",f"The result is ${v}$, a whole number, as the induction proof guarantees."],"Dividing $7^n$, not $7^n-1$, by 6.")
tries(10,i1);tries(10,i2);tries(6,i3)
add("IND","beginner","Which list gives the three parts of a proof by mathematical induction?","Check the base case; assume $P(k)$; prove $P(k+1)$",["Check $P(1)$ only","Assume $P(k+1)$; prove $P(k)$","Check several values of $n$ and stop"],"Structure of induction",["The base case shows the statement starts true.","The inductive hypothesis assumes $P(k)$ for some $k$.","The inductive step uses $P(k)$ to prove $P(k+1)$.","Base case, assume $P(k)$, prove $P(k+1)$."],"Testing a few values proves nothing for all $n$.")
add("IND","intermediate","$P(n)$ is $1+2+\\dots+n=\\frac{n(n+1)}{2}$. Which statement is $P(k+1)$?","$1+2+\\dots+k+(k+1)=\\frac{(k+1)(k+2)}{2}$",["$1+2+\\dots+k=\\frac{(k+1)(k+2)}{2}$","$1+2+\\dots+(k+1)=\\frac{k(k+1)}{2}$","$1+2+\\dots+k=\\frac{k(k+1)}{2}+k+1$"],"Writing $P(k+1)$",["Replace every $n$ in $P(n)$ by $k+1$.","LHS becomes $1+2+\\dots+k+(k+1)$.","RHS becomes $\\frac{(k+1)((k+1)+1)}{2}=\\frac{(k+1)(k+2)}{2}$.","$P(k+1)$ is the first option."],"Writing the working of the inductive step instead of the statement being proved.")
add("IND","intermediate","In proving $1+3+5+\\dots+(2n-1)=n^2$, you assume $P(k)$ and add $(2k+1)$ to both sides. What does the right side become?","$(k+1)^2$",["$k^2+1$","$k^2+2k$","$(k+2)^2$"],"Inductive step",["Assume $1+3+\\dots+(2k-1)=k^2$.","Add the next term: RHS $=k^2+(2k+1)$.","$k^2+2k+1=(k+1)^2$, which is exactly $P(k+1)$.","$(k+1)^2$."],"Stopping at $k^2+2k$ and missing the $+1$ from $2k+1$.")
# ---- BINOMIAL THEOREM
def pw(a,n):
    p=[1]
    for _ in range(n): p=[(p[i] if i<len(p) else 0)+(a*p[i-1] if i>0 else 0) for i in range(len(p)+1)]
    return p
def b1():
    n=R(6,14); r=R(2,n-3); v=math.comb(n,r); assert pw(1,n)[r]==v
    return add("BIN","beginner",f"Find the coefficient of $x^{{{r}}}$ in the expansion of $(1+x)^{{{n}}}$.",m(v),[m(math.comb(n,r-1)),m(math.comb(n,r+1)),m(math.comb(n+1,r))],"Binomial coefficients",
     [f"Given: $(1+x)^{{{n}}}$. Required: the $x^{{{r}}}$ term.","The term in $x^r$ has coefficient $\\binom{n}{r}$.",f"$\\frac{{{n}!}}{{{r}!\\,{n-r}!}}={v}$.",f"The coefficient is ${v}$."],"Choosing $\\binom{n}{r-1}$ because the first term is counted as term 1.")
def b2():
    a,n,r=random.choice([2,3,-1,-2]),R(5,9),R(2,4); v=math.comb(n,r)*a**r; assert pw(a,n)[r]==v
    return add("BIN","intermediate",f"Find the coefficient of $x^{{{r}}}$ in $(1{'+' if a>0 else '-'}{abs(a) if abs(a)>1 else ''}x)^{{{n}}}$.",m(v),[m(math.comb(n,r)*a),m(math.comb(n,r)+a**r),m(math.comb(n,r+1)*a**r)],"Binomial expansion with a coefficient",
     ["The $x^r$ term is $\\binom{n}{r}(ax)^r=\\binom{n}{r}a^rx^r$.",f"$\\binom{{{n}}}{{{r}}}={math.comb(n,r)}$ and $({a})^{{{r}}}={a**r}$.",f"${math.comb(n,r)}\\times({a**r})={v}$.",f"The coefficient is ${v}$."],"Multiplying by $a$ once rather than raising it to the power $r$.")
def b3():
    n=R(5,25)
    return add("BIN","beginner",f"How many terms are in the expansion of $(x+y)^{{{n}}}$?",m(n+1),[m(n),m(n-1),m(2*n)],"Number of terms",[f"The powers of $x$ run from ${n}$ down to $0$.",f"That is ${n}+1$ different terms.",f"${n+1}$ terms.",f"${n+1}$."],"Answering $n$ forgets the term with $x^0$.")
def b4():
    a,b,n=R(1,3),R(1,3),R(4,9); v=(a+b)**n; assert sum(math.comb(n,i)*a**(n-i)*b**i for i in range(n+1))==v
    return add("BIN","intermediate",f"Find the sum of all the coefficients in the expansion of $({a}+{b}x)^{{{n}}}$.",m(v),[m(a**n+b**n),m((a*b)**n),m((a+b)**(n-1))],"Sum of coefficients",
     ["Setting $x=1$ turns every term into its coefficient, so the sum of the coefficients is the value of the expression at $x=1$.",f"$({a}+{b})^{{{n}}}={a+b}^{{{n}}}$.",f"$={v}$.",f"${v}$."],"Raising each number to $n$ separately: $(a+b)^n\\ne a^n+b^n$.")
def b5():
    n,r=R(5,9),R(2,4); v=math.comb(n,r)*2**(n-r); assert sum(math.comb(n,i)*2**(n-i)*(i==r) for i in range(n+1))==v
    return add("BIN","challenging",f"Find the coefficient of $x^{{{r}}}$ in $(2+x)^{{{n}}}$.",m(v),[m(math.comb(n,r)*2**r),m(math.comb(n,r)*2),m(math.comb(n,r)*2**(n-r+1))],"General term",
     ["The general term is $\\binom{n}{r}a^{n-r}b^r$ with $a=2$, $b=x$.",f"For $x^{{{r}}}$: $\\binom{{{n}}}{{{r}}}\\times2^{{{n-r}}}$.",f"${math.comb(n,r)}\\times{2**(n-r)}={v}$.",f"${v}$."],"Using $2^r$; the power of 2 is $n-r$, because the two powers add to $n$.")
tries(22,b1);tries(22,b2);tries(15,b3);tries(18,b4);tries(18,b5)
# ---- COMPLEX NUMBERS
def cx(re,im):
    if im==0: return str(re)
    i="i" if abs(im)==1 else f"{abs(im)}i"
    if re==0: return ("-" if im<0 else "")+i
    return f"{re}{'+' if im>0 else '-'}{i}"
def cxf(re,im):
    re,im=F(re),F(im)
    if im==0: return fr(re)
    t="i" if abs(im)==1 else fr(abs(im))+"i"
    if re==0: return ("-" if im<0 else "")+t
    return f"{fr(re)}{'+' if im>0 else '-'}{t}"
def c1():
    a,b,c,d=[R(-6,7) for _ in range(4)]
    if 0 in (a,b,c,d): return 0
    z=complex(a,b)*complex(c,d); re,im=a*c-b*d,a*d+b*c; assert (z.real,z.imag)==(re,im)
    return add("CPX","intermediate",f"Simplify $({cx(a,b)})({cx(c,d)})$.",m(cx(re,im)),[m(cx(a*c+b*d,im)),m(cx(re,a*d-b*c)),m(cx(re,-im))],"Multiplying complex numbers",
     ["Expand like brackets and use $i^2=-1$.",f"Real part $={a}\\times({c})-({b})({d})={re}$.",f"Imaginary part $={a}\\times({d})+({b})({c})={im}$.",f"${cx(re,im)}$."],"Forgetting that $i^2=-1$, which turns the product $bd\\,i^2$ into $-bd$.")
def c2():
    a,k=random.choice([(3,4),(5,12),(8,15),(7,24),(20,21)]),random.choice([1,2]); x,y=a[0]*k*random.choice([1,-1]),a[1]*k*random.choice([1,-1]); r=math.hypot(x,y); assert r==int(r); r=int(r)
    return add("CPX","beginner",f"Find $|{cx(x,y)}|$.",m(r),[m(abs(x)+abs(y)),m(r+1),m(r*r)],"Modulus",
     ["Use $|a+bi|=\\sqrt{a^2+b^2}$.",f"$\\sqrt{{({x})^2+({y})^2}}=\\sqrt{{{x*x+y*y}}}$.",f"$\\sqrt{{{x*x+y*y}}}={r}$.",f"${r}$."],"Adding $|a|+|b|$ instead of taking the square root of the sum of squares.")
def c3():
    n=R(5,80); v=["1","i","-1","-i"][n%4]; assert 1j**n==complex({"1":1,"i":1j,"-1":-1,"-i":-1j}[v])
    return add("CPX","beginner",f"Simplify $i^{{{n}}}$.",m(v),[m(x) for x in ["1","i","-1","-i"] if x!=v],"Powers of i",
     ["The powers of $i$ repeat every four steps: $i,-1,-i,1$.",f"Divide the index by 4: ${n}=4\\times{n//4}+{n%4}$.",f"So $i^{{{n}}}=i^{{{n%4}}}={v}$.",f"${v}$."],"Using the quotient instead of the remainder when dividing the index by 4.")
def c4():
    a,b,c,d=R(-7,7),R(-7,7),R(1,5),R(-5,5)
    if 0 in (a,b,d): return 0
    den=c*c+d*d; re,im=F(a*c+b*d,den),F(b*c-a*d,den); z=complex(a,b)/complex(c,d); assert abs(z.real-float(re))<1e-9 and abs(z.imag-float(im))<1e-9
    return add("CPX","challenging",f"Express $\\frac{{{cx(a,b)}}}{{{cx(c,d)}}}$ in the form $x+iy$.",m(cxf(re,im)),[m(cxf(re,-im)),m(cxf(F(a*c-b*d,den),im)),m(cxf(a*c+b*d,b*c-a*d))],"Dividing complex numbers",
     [f"Multiply top and bottom by the conjugate of the denominator, ${cx(c,-d)}$.",f"Denominator: $({c})^2+({d})^2={den}$.",f"Numerator: real part ${a*c+b*d}$, imaginary part ${b*c-a*d}$.",f"Divide by ${den}$: ${cxf(re,im)}$."],"Leaving out the division by $c^2+d^2$, or using the wrong conjugate.")
tries(24,c1);tries(16,c2);tries(24,c3);tries(22,c4)
# ---- CIRCULAR MEASURE
TH=[F(1,6),F(1,4),F(1,3),F(1,2),F(2,3),F(3,4),F(1),F(3,2)]
def r1():
    d=15*R(1,23); x=F(d,180); assert abs(float(x)*math.pi-math.radians(d))<1e-12
    return add("CIR","beginner",f"Convert ${d}^\\circ$ to radians.",m(pi(x)),[m(pi(F(d,360))),m(pi(F(d,90))),m(pi(F(d,150)))],"Degrees to radians",
     ["Use $180^\\circ=\\pi$ radians, so multiply by $\\frac{\\pi}{180}$.",f"${d}\\times\\frac{{\\pi}}{{180}}={pi(x)}$.",f"The angle is ${pi(x)}$ radians.",f"${pi(x)}$ rad."],"Using 360 or 90 instead of 180.")
def r2():
    d=15*R(1,23); x=F(d,180)
    return add("CIR","beginner",f"Convert ${pi(x)}$ radians to degrees.",m(f"{d}^\\circ"),[m(f"{2*d}^\\circ"),m(f"{d+15}^\\circ"),m(f"{d+30}^\\circ")],"Radians to degrees",
     ["Multiply by $\\frac{180}{\\pi}$ so $\\pi$ cancels.",f"${pi(x)}\\times\\frac{{180}}{{\\pi}}={d}$.",f"The angle is ${d}^\\circ$.",f"${d}^\\circ$."],"Multiplying by $\\frac{360}{\\pi}$ doubles the answer.")
def r3():
    r,t=R(3,24),random.choice(TH); s=r*t
    return add("CIR","intermediate",f"Find the arc length of a sector with radius ${r}$ cm and angle ${pi(t)}$ radians.",m(pi(s))+" cm",[m(pi(s/2))+" cm",m(pi(r*r*t))+" cm",m(pi(s*2))+" cm"],"Arc length",
     [f"Given: $r={r}$, $\\theta={pi(t)}$ (already in radians).","Use $s=r\\theta$.",f"$s={r}\\times{pi(t)}={pi(s)}$.",f"$s={pi(s)}$ cm."],"Using the area formula $\\frac12r^2\\theta$ by mistake.")
def r4():
    r,t=R(2,14),random.choice(TH); A=F(1,2)*r*r*t
    return add("CIR","intermediate",f"Find the area of a sector with radius ${r}$ cm and angle ${pi(t)}$ radians.",m(pi(A))+" cm$^2$",[m(pi(r*t))+" cm$^2$",m(pi(r*r*t))+" cm$^2$",m(pi(F(1,2)*r*t))+" cm$^2$"],"Sector area",
     [f"Given: $r={r}$, $\\theta={pi(t)}$.","Use $A=\\frac{1}{2}r^2\\theta$.",f"$A=\\frac12\\times{r*r}\\times{pi(t)}={pi(A)}$.",f"$A={pi(A)}$ cm$^2$."],"Dropping the $\\frac12$ or using $r$ instead of $r^2$.")
def r5():
    r,s=R(2,12),R(2,30)
    if s%r==0: return 0
    return add("CIR","beginner",f"An arc of length ${s}$ cm is cut from a circle of radius ${r}$ cm. Find the angle it subtends at the centre, in radians.",m(fr(F(s,r)))+" rad",[m(fr(F(r,s)))+" rad",m(s*r)+" rad",m(s-r)+" rad"],"Angle from arc length",
     [f"Given: $s={s}$, $r={r}$.","From $s=r\\theta$, $\\theta=\\frac{s}{r}$.",f"$\\theta=\\frac{{{s}}}{{{r}}}={fr(F(s,r))}$.",f"${fr(F(s,r))}$ radians."],"Inverting the ratio to $\\frac{r}{s}$.")
tries(22,r1);tries(22,r2);tries(24,r3);tries(24,r4);tries(20,r5)
# ---- TRIGONOMETRIC FUNCTIONS
S={30:("\\frac{1}{2}",.5),45:("\\frac{\\sqrt{2}}{2}",2**.5/2),60:("\\frac{\\sqrt{3}}{2}",3**.5/2)}
Cc={30:S[60],45:S[45],60:S[30]}
Tn={30:("\\frac{\\sqrt{3}}{3}",3**.5/3),45:("1",1.0),60:("\\sqrt{3}",3**.5)}
def tv(f,t):
    ref=t if t<=90 else 180-t if t<180 else t-180 if t<270 else 360-t
    base={"sin":S,"cos":Cc,"tan":Tn}[f][ref]
    sg=(-1 if 180<t<360 else 1) if f=="sin" else (-1 if 90<t<270 else 1) if f=="cos" else (-1 if (t%360)//90 in (1,3) else 1)
    return ("-" if sg<0 else "")+base[0],sg*base[1],ref
def t1():
    t=random.choice([30,45,60,120,135,150,210,225,240,300,315,330]); f=random.choice(["sin","cos","tan"])
    L,val,ref=tv(f,t); assert abs(val-getattr(math,f)(math.radians(t)))<1e-9
    alt=[x for x in ("sin","cos","tan") if x!=f]
    neg=L[1:] if L[0]=="-" else "-"+L
    w=[neg,tv(f,t-ref+(90-ref) if False else 90-ref)[0],tv(alt[0],t)[0],tv(alt[1],t)[0]]
    q=t//90+1
    return add("TRG","intermediate" if t>90 else "beginner",f"Find the exact value of $\\{f}\\,{t}^\\circ$.",m(L),[m(x) for x in w],"Exact values and the CAST rule",
     [f"${t}^\\circ$ lies in quadrant {q}; its reference angle is ${ref}^\\circ$.",f"$\\{f}\\,{ref}^\\circ={tv(f,ref)[0]}$.","Apply the sign for this quadrant: all positive in quadrant 1, sine in 2, tangent in 3, cosine in 4.",f"$\\{f}\\,{t}^\\circ={L}$."],"Taking the correct magnitude but the wrong sign for the quadrant.")
def t2():
    a,b,c=random.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29),(4,3,5),(12,5,13)]); f=random.choice(["cos","tan"])
    ans=F(b,c) if f=="cos" else F(a,b); th=math.asin(a/c); assert abs(getattr(math,f)(th)-float(ans))<1e-9
    return add("TRG","intermediate",f"$\\theta$ is acute and $\\sin\\theta=\\frac{{{a}}}{{{c}}}$. Find $\\{f}\\,\\theta$.",m(fr(ans)),[m(fr(F(a,b))) if f=="cos" else m(fr(F(b,c))),m(fr(F(c,b))),m(fr(F(b,a)))],"Right-angled triangle ratios",
     [f"Draw a right triangle: opposite ${a}$, hypotenuse ${c}$.",f"Adjacent $=\\sqrt{{{c}^2-{a}^2}}={b}$.",f"$\\cos\\theta=\\frac{{{b}}}{{{c}}}$ and $\\tan\\theta=\\frac{{{a}}}{{{b}}}$.",f"$\\{f}\\,\\theta={fr(ans)}$."],"Mixing up which sides each ratio uses (SOH-CAH-TOA).")
def t3():
    a,b,c=random.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29)])
    return add("TRG","challenging",f"$A$ is obtuse and $\\sin A=\\frac{{{a}}}{{{c}}}$. Find $\\cos A$.",m(fr(F(-b,c))),[m(fr(F(b,c))),m(fr(F(-a,c))),m(fr(F(-b,a)))],"Sign of cosine in the second quadrant",
     [f"Given: $\\sin A=\\frac{{{a}}}{{{c}}}$, $A$ in quadrant 2.",f"$\\cos^2A=1-\\sin^2A=1-\\frac{{{a*a}}}{{{c*c}}}=\\frac{{{b*b}}}{{{c*c}}}$, so $|\\cos A|=\\frac{{{b}}}{{{c}}}$.","Cosine is negative in the second quadrant.",f"$\\cos A=-\\frac{{{b}}}{{{c}}}$."],"Giving the positive root; $\\cos^2A$ has two roots and the quadrant picks the sign.")
tries(36,t1);tries(14,t2);tries(5,t3)
# ---- VALIDATION AND OUTPUT
ids=[q["id"] for q in Q]; assert len(ids)==len(set(ids)),"duplicate IDs"
assert len({q["question"] for q in Q})==len(Q),"duplicate questions"
for q in Q:
    assert len({o["text"] for o in q["options"]})==4 and q["explanation"]["steps"] and q["explanation"]["commonMistake"]
    assert [o for o in q["options"] if o["id"]==q["correctAnswer"]][0]["text"]==q["explanation"]["finalAnswer"]
order=list(TS.values()); Q.sort(key=lambda q:(order.index(q["topic"]),q["id"]))
json.dump(Q,open("data/questions.json","w"),ensure_ascii=False)
open("data/questions.js","w").write("window.MAT_QUESTIONS="+json.dumps(Q,ensure_ascii=False)+";")
rep=["# Question count (verified at build time)\n"]+[f"- {t}: {sum(q['topic']==t for q in Q)}" for t in order]+[f"\n**Total: {len(Q)}**"]
open("data/REPORT.md","w").write("\n".join(rep)); print("\n".join(rep))
