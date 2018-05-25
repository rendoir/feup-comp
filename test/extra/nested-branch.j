.class public nestedBranch
.super java/lang/Object

.method public static sign(I)I
.limit locals 1
.limit stack 1

iload_0
ifge else1
iconst_m1
istore_0
goto end1
else1:
iload_0
ifne else2
iconst_0
istore_0
goto end2
else2:
iconst_1
istore_0
end2:
end1:
iload_0
ireturn

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 3
.limit stack 2

bipush -10
istore_0
bipush 10
istore_1
iload_0
iload_1
iadd
istore_2
iload_0
invokestatic nestedBranch/sign(I)I
istore_0
iload_2
invokestatic nestedBranch/sign(I)I
istore_2
iload_1
invokestatic nestedBranch/sign(I)I
istore_1
iload_0
invokestatic io/println(I)V
iload_2
invokestatic io/println(I)V
iload_1
invokestatic io/println(I)V
return

.end method
