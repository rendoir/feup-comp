.class public inputAsOutput
.super java/lang/Object

.method public static f(I)I
.limit locals 1
.limit stack 1

iload_0
ireturn

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 1
.limit stack 1

iconst_1
invokestatic inputAsOutput/f(I)I
istore_0
iload_0
invokestatic io/println(I)V
return

.end method
