.class public registerTest
.super java/lang/Object

.method public static f(I)I
.limit locals 1
.limit stack 2

iload_0
iconst_1
iadd
istore_0
iload_0
iconst_2
iadd
istore_0
iload_0
iconst_3
iadd
istore_0
iload_0
iconst_1
iadd
istore_0
iload_0
ireturn

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 1
.limit stack 1

iconst_1
invokestatic registerTest/f(I)I
istore_0
iload_0
invokestatic io/println(I)V
return

.end method
