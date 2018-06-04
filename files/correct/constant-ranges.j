.class public constantRanges
.super java/lang/Object

.method public static f()V
.limit locals 7
.limit stack 1

iconst_5
istore_0
iconst_m1
istore_1
bipush 6
istore_2
sipush 128
istore_3
sipush -129
istore 4
ldc 32768
istore 5
ldc -32769
istore 6
iload_0
invokestatic io/println(I)V
iload_1
invokestatic io/println(I)V
iload_2
invokestatic io/println(I)V
iload_3
invokestatic io/println(I)V
iload 4
invokestatic io/println(I)V
iload 5
invokestatic io/println(I)V
iload 6
invokestatic io/println(I)V
return

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 1
.limit stack 0

invokestatic constantRanges/f()V
return

.end method
