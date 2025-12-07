
from math import log2

"""
Register A: 41644071
Register B: 0
Register C: 0

Program: 2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0
		 C O C O C O C O C O C O C O C O	
		 1	 2	 3	 4	 5	 6   !   J  
								 
 Output Register B
 
 1. B = A % 8
 2. B = B ^ 2
 3. C = A / (2**B)
 4. B = B ^ 7
 5. B = B ^ C
 6. A = A / (2**3)
 -> Output Register b
 
 
 Falls in Register B 2 stehen soll:
 
 A = A / 8 
 A ist in Größenordnung 2,8 * 10**14
 
 Wenn als erstes eine "2" ausgegeben werden soll:
 
 1. B zwischen 0 und 7 
 2. Dann B xor 2 B +- 2, je nachdem ob bit gesetzt war
 3. C = A / 4
 4. B xor 7 -> 5 (Erste Iteration)
 5. B = B XOR C 
 
 -> Kann alles als Bit-Shift Operation dargestellt werden ?!
 
 
 1 + 2   B = (A % 8)^ 2 <=> (A & 7)^2 
	-> B ist zwischen 0 und 7
 3. C = A >> B
 4. B = B ^ 7
 5. B = B ^ C <=> 
 6. A = A / 8  <=> A >> 3

 Kann ich immer genau drei byte konstruieren, die mir die Zahl ausgeben?

 Eher nicht, weil A ja um B geshifter wird um C zu ergeben

"""

print((0 ^ 2) ^ 7)


print(all(
    [x >> 3 == int(x / 8) for x in range(1000)]
))

print(all(
    [x % 8  == x & 7 for x in range(1000)]
))

print([x &7 ^ 2 for x in range(0,33)])


print(all([
    all(
        [A >> x == int(A / 2**x) for x in range(0,8)]
    ) for A in range(0,1000)
] ))

print(((2 << (16 * 3 +1) )) - (2 << (16 * 3) ) ) 
print(2 << 7)