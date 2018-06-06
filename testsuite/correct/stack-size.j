.class public stackSize
.super java/lang/Object

.method public static f(I)V
.limit locals 1
.limit stack 5

iload_0
iload_0
iload_0
iload_0
iload_0
invokestatic stackSize/h(IIII)I
if_icmple else1
ldc "Greater"
invokestatic io/println(Ljava/lang/String;)V
goto end1
else1:
ldc "Not greater"
invokestatic io/println(Ljava/lang/String;)V
end1:
return

.end method

.method public static g(I)I
.limit locals 1
.limit stack 5

iload_0
iload_0
iload_0
iload_0
iload_0
invokestatic stackSize/h(IIII)I
imul
istore_0
iload_0
ireturn

.end method

.method public static h(IIII)I
.limit locals 4
.limit stack 2

iload_0
iload_1
iadd
istore_0 ; y could also be assigned to local 1
iload_0
iload_2
iadd
istore_0
iload_0
iload_3
iadd
istore_0
iload_0
ireturn

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 1
.limit stack 1

iconst_m1
istore_0
iload_0
invokestatic stackSize/f(I)V
return

.end method
