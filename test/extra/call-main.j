.class public callMain
.super java/lang/Object

.field static x I = 1

.method public static f()V
.limit locals 0
.limit stack 2

getstatic callMain/x I
ifle end_if
getstatic callMain/x I
iconst_1
isub
putstatic callMain/x I
aconst_null
invokestatic callMain/main([Ljava/lang/String;)V
end_if:
return

.end method

.method public static main([Ljava/lang/String;)V
.limit locals 1
.limit stack 1

ldc "Call main"
invokestatic io/println(Ljava/lang/String;)V
invokestatic callMain/f()V
return

.end method
