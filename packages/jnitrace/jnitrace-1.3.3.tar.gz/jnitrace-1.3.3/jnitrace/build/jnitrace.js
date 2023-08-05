(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "DestroyJavaVM",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThread",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
    {
        "name": "DetachCurrentThread",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetEnv",
        "args": [
            "JavaVM*",
            "void**",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThreadAsDaemon",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
]

},{}],2:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved3",
        "args": [],
        "ret": null
    },
    {
        "name": "GetVersion",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jint"
    },
    {
        "name": "DefineClass",
        "args": [
            "JNIEnv*",
            "char*",
            "jobject",
            "jbyte*",
            "jsize"
        ],
        "ret": "jclass"
    },
    {
        "name": "FindClass",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jclass"
    },
    {
        "name": "FromReflectedMethod",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "FromReflectedField",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "ToReflectedMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetSuperclass",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsAssignableFrom",
        "args": [
            "JNIEnv*",
            "jclass",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "ToReflectedField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "Throw",
        "args": [
            "JNIEnv*",
            "jthrowable"
        ],
        "ret": "jint"
    },
    {
        "name": "ThrowNew",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*"
        ],
        "ret": "jint"
    },
    {
        "name": "ExceptionOccurred",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jthrowable"
    },
    {
        "name": "ExceptionDescribe",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionClear",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "FatalError",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "PushLocalFrame",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "PopLocalFrame",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "DeleteGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "DeleteLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "IsSameObject",
        "args": [
            "JNIEnv*",
            "jobject",
            "jobject"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "EnsureLocalCapacity",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AllocObject",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObject",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetObjectClass",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsInstanceOf",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallStaticObjectMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticBooleanMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticByteMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticCharMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticShortMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticIntMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticLongMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticFloatMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticDoubleMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticVoidMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "NewString",
        "args": [
            "JNIEnv*",
            "jchar*",
            "jsize"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewStringUTF",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringUTFLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "char*"
    },
    {
        "name": "ReleaseStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetArrayLength",
        "args": [
            "JNIEnv*",
            "jarray"
        ],
        "ret": "jsize"
    },
    {
        "name": "NewObjectArray",
        "args": [
            "JNIEnv*",
            "jsize",
            "jclass",
            "jobject"
        ],
        "ret": "jobjectArray"
    },
    {
        "name": "GetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize"
        ],
        "ret": "jobject"
    },
    {
        "name": "SetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "NewBooleanArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbooleanArray"
    },
    {
        "name": "NewByteArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbyteArray"
    },
    {
        "name": "NewCharArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jcharArray"
    },
    {
        "name": "NewShortArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jshortArray"
    },
    {
        "name": "NewIntArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jintArray"
    },
    {
        "name": "NewLongArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jlongArray"
    },
    {
        "name": "NewFloatArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jfloatArray"
    },
    {
        "name": "NewDoubleArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jdoubleArray"
    },
    {
        "name": "GetBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jboolean*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jboolean*"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jboolean*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jboolean*"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jboolean*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jboolean*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "ReleaseBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jbyte*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jchar*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jshort*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jint*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jlong*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jfloat*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jdouble*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "GetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "GetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "GetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "GetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "GetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "RegisterNatives",
        "args": [
            "JNIEnv*",
            "jclass",
            "JNINativeMethod*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "UnregisterNatives",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorEnter",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorExit",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "GetJavaVM",
        "args": [
            "JNIEnv*",
            "JavaVM**"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStringRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringUTFRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetPrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "ReleasePrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "void*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jweak"
    },
    {
        "name": "DeleteWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jweak"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionCheck",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewDirectByteBuffer",
        "args": [
            "JNIEnv*",
            "void*",
            "jlong"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetDirectBufferAddress",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "GetDirectBufferCapacity",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetObjectRefType",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobjectRefType"
    }
]

},{}],3:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorARM(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorARM.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new ArmWriter(code, {
      pc: text
    });
    var dataOffset = 0; // str r0, [pc, #0x400]

    cw.putInstruction(0xe58f0400); // str r1, [pc, #0x400]

    cw.putInstruction(0xe58f1400); // str r2, [pc, #0x400]

    cw.putInstruction(0xe58f2400); // str r3, [pc, #0x400]

    cw.putInstruction(0xe58f3400); // str lr, [pc, #0x400]

    cw.putInstruction(0xe58fe400); // ldr r0, [pc, #0x3e4]

    cw.putInstruction(0xe59f03e4); // blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, 0x3e0]

    cw.putInstruction(0xe59f13e8); // ldr r2, [pc, 0x3e0]

    cw.putInstruction(0xe59f23e8); // ldr r3, [pc, 0x3e0]

    cw.putInstruction(0xe59f33e8); //blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, #0x3e4]

    cw.putInstruction(0xe59f13e4); // bx r1

    cw.putInstruction(0xe12fff11);
    cw.flush();
  }); // required to prevent a crash

  Interceptor.attach(text.add(56), function () {});
};

JNIEnvInterceptorARM.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorARM.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "double" || retType === "int64") {
    retval = registers.r1.toString().substring(2) + registers.r0.toString().substring(2);
  }

  return retval;
};

module.exports = JNIEnvInterceptorARM;

},{"../../utils/types":14,"../jni_env_interceptor":6}],4:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorARM64(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

var keepforever;
JNIEnvInterceptorARM64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM64.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  //text = Memory.alloc(Process.pageSize);
  Memory.writePointer(text.add(0x400), parser);
  keepforever = text;
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new Arm64Writer(code, {
      pc: text
    }); // adrp x0, #0

    cw.putInstruction(0x90000000); // back up all registers - just to be safe

    for (var i = 1; i < 31; i++) {
      var ins = 0xF9000000; // src reg

      ins += i;
      var offset = 0x408 + i * Process.pointerSize; // dst address

      ins += offset / 2 << 8; // str x<n>, [x0, #<offset>]

      cw.putInstruction(ins);
    } // ldr x0, [x0, #0x400]


    cw.putInstruction(0xF9420000); // blr x0

    cw.putInstruction(0xD63F0000);
    cw.putPushRegReg("x0", "sp"); // adrp x0, #0

    cw.putInstruction(0x90000000); // restore all registers - apart from lr and sp

    for (var i = 1; i < 30; i++) {
      var ins = 0xF9400000; // src reg

      ins += i;
      var offset = 0x408 + i * Process.pointerSize; // dst address

      ins += offset / 2 << 8; // ldr x<n>, [x0, #<offset>]

      cw.putInstruction(ins);
    }

    cw.putPopRegReg("x0", "sp"); // blr x0

    cw.putInstruction(0xD63F0000); // adrp x1, #0

    cw.putInstruction(0x90000001); // ldr x2, [x1, #0x4f8]

    cw.putInstruction(0xF9427C22); // br x2

    cw.putInstruction(0xD61F0040);
    cw.flush();
  }); // required to prevent a crash

  Interceptor.attach(text, function () {});
};

JNIEnvInterceptorARM64.prototype.setUpVaListArgExtract = function (vaList) {
  this.stack = Memory.readPointer(vaList);
  this.stackIndex = 0;
  this.grTop = Memory.readPointer(vaList.add(Process.pointerSize));
  this.vrTop = Memory.readPointer(vaList.add(Process.pointerSize * 2));
  this.grOffs = Memory.readS32(vaList.add(Process.pointerSize * 3));
  this.grOffsIndex = 0;
  this.vrOffs = Memory.readS32(vaList.add(Process.pointerSize * 3 + 4));
  this.vrOffsIndex = 0;
};

JNIEnvInterceptorARM64.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = NULL;

  if (method.params[paramId] === "float" || method.params[paramId] === "double") {
    if (this.vrOffsIndex < 8) {
      currentPtr = this.vrTop.add(this.vrOffs).add(this.vrOffsIndex * Process.pointerSize * 2);
      this.vrOffsIndex++;
    } else {
      currentPtr = this.stack.add(this.stackIndex * Process.pointerSize);
      this.stackIndex++;
    }
  } else {
    if (this.grOffsIndex < 4) {
      currentPtr = this.grTop.add(this.grOffs).add(this.grOffsIndex * Process.pointerSize);
      this.grOffsIndex++;
    } else {
      currentPtr = this.stack.add(this.stackIndex * Process.pointerSize);
      this.stackIndex++;
    }
  }

  return currentPtr;
};

JNIEnvInterceptorARM64.prototype.resetVaListArgExtract = function () {
  this.stack = NULL;
  this.stackIndex = 0;
  this.grTop = NULL;
  this.vrTop = NULL;
  this.grOffs = NULL;
  this.grOffsIndex = 0;
  this.vrOffs = NULL;
  this.vrOffsIndex = 0;
};

JNIEnvInterceptorARM64.prototype.processVaListRetVal = function (retType, retval, registers) {
  return retval;
};

module.exports = JNIEnvInterceptorARM64;

},{"../../utils/types":14,"../jni_env_interceptor":6}],5:[function(require,module,exports){
var JAVA_VM_METHODS = require("../data/java_vm.json");

var Types = require("../utils/types");

function JavaVMInterceptor(references, threads, jniEnvInterceptor) {
  this.references = references;
  this.threads = threads;
  this.jniEnvInterceptor = jniEnvInterceptor;
  this.shadowJavaVM = NULL;
}

JavaVMInterceptor.prototype.isInitialised = function () {
  return !this.shadowJavaVM.isNull();
};

JavaVMInterceptor.prototype.get = function () {
  return this.shadowJavaVM;
};

JavaVMInterceptor.prototype.createJavaVMIntercept = function (id, methodAddr) {
  var self = this;
  var method = JAVA_VM_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);
    fridaArgs.push(ftype);
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = Process.getCurrentThreadId();
    var localArgs = [].slice.call(arguments);
    var javaVM = self.threads.getJavaVM();
    var jniEnv = NULL;
    localArgs[0] = javaVM;
    var ret = nativeFunction.apply(null, localArgs);

    if (method.name === "GetEnv" || method.name === "AttachCurrentThread" || method.name === "AttachCurrentThreadAsDaemon") {
      if (ret === 0) {
        self.threads.setJNIEnv(threadId, Memory.readPointer(localArgs[1]));
      }

      if (!self.jniEnvInterceptor.isInitialised()) {
        jniEnv = self.jniEnvInterceptor.create();
      } else {
        jniEnv = self.jniEnvInterceptor.get();
      }

      Memory.writePointer(localArgs[1], jniEnv);
    }

    return ret;
  }, fridaRet, fridaArgs);
  this.references.add(nativeCallback);
  return nativeCallback;
};

JavaVMInterceptor.prototype.create = function () {
  var javaVMOffset = 3;
  var javaVMLength = 8;
  var threadId = Process.getCurrentThreadId();
  var javaVM = this.threads.getJavaVM(threadId);
  var newJavaVMStruct = Memory.alloc(Process.pointerSize * javaVMLength);
  this.references.add(newJavaVMStruct);
  var newJavaVM = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJavaVM, newJavaVMStruct);

  for (var i = javaVMOffset; i < javaVMLength; i++) {
    var offset = i * Process.pointerSize;
    var javaVMStruct = Memory.readPointer(javaVM);
    var methodAddr = Memory.readPointer(javaVMStruct.add(offset));
    var callback = this.createJavaVMIntercept(i, ptr(methodAddr));
    Memory.writePointer(newJavaVMStruct.add(offset), callback);
  }

  this.shadowJavaVM = newJavaVM;
  return newJavaVM;
};

module.exports = JavaVMInterceptor;

},{"../data/java_vm.json":1,"../utils/types":14}],6:[function(require,module,exports){
var JNI_ENV_METHODS = require("../data/jni_env.json");

var Types = require("../utils/types");

var JavaMethod = require("../utils/java_method");

function JNIEnvInterceptor(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.javaVMInterceptor = NULL;
}

JNIEnvInterceptor.prototype.shadowJNIEnv = null;
JNIEnvInterceptor.prototype.methods = {};
JNIEnvInterceptor.prototype.fastMethodLookup = {};

JNIEnvInterceptor.prototype.isInitialised = function () {
  return this.shadowJNIEnv !== null;
};

JNIEnvInterceptor.prototype.get = function () {
  return this.shadowJNIEnv;
};

JNIEnvInterceptor.prototype.createJNIIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);

    if (ftype !== "va_list") {
      fridaArgs.push(ftype);
    }
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = Process.getCurrentThreadId();
    var localArgs = [].slice.call(arguments);
    var jniEnv = self.threads.getJNIEnv(threadId);
    var context = null;

    if (this) {
      context = this.context;
    }

    localArgs[0] = jniEnv;
    var ret = nativeFunction.apply(null, localArgs);
    var add = null;

    if (method.args[method.args.length - 1] === "jvalue*") {
      add = self.methods[ptr(localArgs[2])].javaParams;
      var jvalues = ptr(localArgs[method.args.length - 1]);
      localArgs = localArgs.slice(0, -1);

      for (var i = 0; i < add.length; i++) {
        var val = NULL;
        var type = Types.convertNativeJTypeToFridaType(add[i]);
        var val = self.readValue(jvalues.add(8 * i), type);
        localArgs.push(val);
      }
    }

    self.transport.trace(method, localArgs, ret, context, add);

    if (method.name === "GetMethodID" || method.name === "GetStaticMethodID") {
      var signature = Memory.readCString(localArgs[3]);
      var types = new JavaMethod(signature);
      var fridaTypes = {
        params: [],
        javaParams: [],
        ret: NULL
      };

      for (var i = 0; i < types.params.length; i++) {
        var nativeJType = Types.convertJTypeToNativeJType(types.params[i]);
        var fridaType = Types.convertNativeJTypeToFridaType(nativeJType);
        fridaTypes.params.push(fridaType);
        fridaTypes.javaParams.push(Types.convertJTypeToNativeJType(types.params[i]));
      }

      var jTypeRet = Types.convertJTypeToNativeJType(types.ret);
      fridaTypes.ret = Types.convertNativeJTypeToFridaType(jTypeRet);
      self.methods[ret] = fridaTypes;
    } else if (method.name === "GetJavaVM") {
      var javaVM = NULL;

      if (ret === 0) {
        self.threads.setJavaVM(Memory.readPointer(localArgs[1]));
      }

      if (!self.javaVMInterceptor.isInitialised()) {
        javaVM = self.javaVMInterceptor.create();
      } else {
        javaVM = self.javaVMInterceptor.get();
      }

      Memory.writePointer(localArgs[1], javaVM);
    } else if (method.name === "RegisterNatives") {
      var methods = localArgs[2];
      var size = localArgs[3];

      for (var i = 0; i < size * 3; i += 3) {
        var offset = (i + 2) * Process.pointerSize;
        var addr = Memory.readPointer(methods.add(offset));
        Interceptor.attach(addr, {
          onEnter: function (args) {
            if (!self.threads.hasJNIEnv(this.threadId)) {
              self.threads.setJNIEnv(this.threadId, ptr(args[0]));
            }

            args[0] = ptr(self.shadowJNIEnv);
          }
        });
      }
    }

    return ret;
  }, fridaRet, fridaArgs);
  this.references.add(nativeCallback);
  return nativeCallback;
};

JNIEnvInterceptor.prototype.createJNIVarArgIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var text = Memory.alloc(Process.pageSize);
  var data = Memory.alloc(Process.pageSize);
  var vaArgsCallback = NULL;
  var mainCallback = NULL;
  this.references.add(text);
  this.references.add(data);
  vaArgsCallback = new NativeCallback(function () {
    var callbackParams = [];
    var originalParams = [];
    var methodId = arguments[2];
    var vaArgs = self.methods[methodId];

    if (self.fastMethodLookup[methodId]) {
      return self.fastMethodLookup[methodId];
    }

    for (var i = 0; i < method.args.length - 1; i++) {
      var fridaType = Types.convertNativeJTypeToFridaType(method.args[i]);
      callbackParams.push(fridaType);
      originalParams.push(fridaType);
    }

    originalParams.push("...");

    for (var i = 0; i < vaArgs.params.length; i++) {
      if (vaArgs.params[i] === "float") {
        callbackParams.push("double");
      } else {
        callbackParams.push(vaArgs.params[i]);
      }

      originalParams.push(vaArgs.params[i]);
    }

    var retType = Types.convertNativeJTypeToFridaType(method.ret);
    mainCallback = new NativeCallback(function () {
      var threadId = this.threadId;
      var localArgs = [].slice.call(arguments);
      var jniEnv = self.threads.getJNIEnv(threadId);
      localArgs[0] = jniEnv;
      var ret = new NativeFunction(methodAddr, retType, originalParams).apply(null, localArgs);
      self.transport.trace(method, localArgs, ret, this.context, vaArgs.javaParams);
      return ret;
    }, retType, callbackParams);
    self.references.add(mainCallback);
    self.fastMethodLookup[methodId] = mainCallback;
    return mainCallback;
  }, "pointer", ["pointer", "pointer", "pointer"]);
  this.references.add(vaArgsCallback);
  self.buildVaArgParserShellcode(text, data, vaArgsCallback);
  return text;
};

JNIEnvInterceptor.prototype.processVaListRetVal = function (retType, retval, registers) {
  return retval;
};

JNIEnvInterceptor.prototype.createJNIVaListIntercept = function (id, methodAddr) {
  var self = this;
  var methodData = JNI_ENV_METHODS[id];
  var retType = Types.convertNativeJTypeToFridaType(methodData.ret);
  Interceptor.attach(methodAddr, {
    onEnter: function (args) {
      var threadId = this.threadId;
      this.shadowJNIEnv = self.threads.getJNIEnv(threadId);
      this.localJNIEnv = ptr(args[0]);

      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        this.methodId = ptr(args[2]);
        var vaList = ptr(args[3]);
        this.args = [this.localJNIEnv, args[1], this.methodId];
        this.ret = NULL;
        var method = self.methods[this.methodId];

        if (!method) {
          return;
        }

        self.setUpVaListArgExtract(vaList);

        for (var i = 0; i < method.params.length; i++) {
          var currentPtr = self.extractVaListArgValue(method, i);
          var val = self.readValue(currentPtr, method.params[i], true);
          this.args.push(val);
        }

        self.resetVaListArgExtract();
        args[0] = this.shadowJNIEnv;
      }
    },
    onLeave: function (originalRet) {
      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        var ret = NULL;
        var retval = self.processVaListRetVal(retType, ptr(originalRet), this.context);

        if (retType === "int8") {
          ret = retval.toInt32();
        } else if (retType === "int16") {
          ret = retval.toInt32();
        } else if (retType === "uint16") {
          ret = retval.toInt32();
        } else if (retType === "int32") {
          ret = retval.toInt32();
        } else if (retType === "int64") {
          ret = uint64("0x" + retval.toString());
        } else if (retType === "float") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeS32(buf, retval.toInt32());
          ret = Memory.readFloat(buf);
        } else if (retType === "double") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeU64(buf, uint64("0x" + retval.toString()));
          ret = Memory.readDouble(buf);
        }

        var add = self.methods[this.methodId].javaParams;
        self.transport.trace(methodData, this.args, ret, this.context, add);
      }
    }
  });
  return methodAddr;
};

JNIEnvInterceptor.prototype.readValue = function (currentPtr, type, extend) {
  var val = NULL;

  if (type === "char") {
    val = Memory.readS8(currentPtr);
  } else if (type === "int16") {
    val = Memory.readS16(currentPtr);
  } else if (type === "uint16") {
    val = Memory.readU16(currentPtr);
  } else if (type === "int") {
    val = Memory.readS32(currentPtr);
  } else if (type === "int64") {
    val = Memory.readS64(currentPtr);
  } else if (type === "float") {
    if (extend) {
      val = Memory.readDouble(currentPtr);
    } else {
      val = Memory.readFloat(currentPtr);
    }
  } else if (type === "double") {
    val = Memory.readDouble(currentPtr);
  } else if (type === "pointer") {
    val = Memory.readPointer(currentPtr);
  }

  return val;
};

JNIEnvInterceptor.prototype.setJavaVMInterceptor = function (javaVMInterceptor) {
  this.javaVMInterceptor = javaVMInterceptor;
};

JNIEnvInterceptor.prototype.create = function () {
  var threadId = Process.getCurrentThreadId();
  var jniEnv = this.threads.getJNIEnv(threadId);
  var jniEnvOffset = 4;
  var jniEnvLength = 232;
  var newJNIEnvStruct = Memory.alloc(Process.pointerSize * jniEnvLength);
  this.references.add(newJNIEnvStruct);
  var newJNIEnv = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJNIEnv, newJNIEnvStruct);
  this.references.add(newJNIEnv);

  for (var i = jniEnvOffset; i < jniEnvLength; i++) {
    var method = JNI_ENV_METHODS[i];
    var offset = i * Process.pointerSize;
    var jniEnvStruct = Memory.readPointer(jniEnv);
    var methodAddr = Memory.readPointer(jniEnvStruct.add(offset));

    if (method.args[method.args.length - 1] === "...") {
      var callback = this.createJNIVarArgIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else if (method.args[method.args.length - 1] === "va_list") {
      var callback = this.createJNIVaListIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else {
      var callback = this.createJNIIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    }
  }

  this.shadowJNIEnv = newJNIEnv;
  return newJNIEnv;
};

module.exports = JNIEnvInterceptor;

},{"../data/jni_env.json":2,"../utils/java_method":12,"../utils/types":14}],7:[function(require,module,exports){
function JNIThreadManager() {
  this.threads = {};
  this.shadowJavaVM = NULL;
}

JNIThreadManager.prototype.createEntry = function (threadId) {
  if (!this.threads[threadId]) {
    this.threads[threadId] = {
      'jniEnv': NULL
    };
  }

  return this.threads[threadId];
};

JNIThreadManager.prototype.getJavaVM = function () {
  return this.shadowJavaVM;
};

JNIThreadManager.prototype.hasJavaVM = function () {
  return !this.shadowJavaVM.isNull();
};

JNIThreadManager.prototype.setJavaVM = function (javaVM) {
  this.shadowJavaVM = javaVM;
};

JNIThreadManager.prototype.getJNIEnv = function (threadId) {
  var entry = this.createEntry(threadId);
  return entry.jniEnv;
};

JNIThreadManager.prototype.hasJNIEnv = function (threadId) {
  return !this.getJNIEnv(threadId).isNull();
};

JNIThreadManager.prototype.setJNIEnv = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);
  entry.jniEnv = jniEnv;
};

JNIThreadManager.prototype.needsJNIEnvUpdate = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);

  if (!entry.jniEnv.equals(jniEnv)) {
    return true;
  }

  return false;
};

module.exports = JNIThreadManager;

},{}],8:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

function JNIEnvInterceptorX64(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
}

JNIEnvInterceptorX64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptor.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0;
    var xmmOffset = 0;
    var regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9", "rax", "rbx", "r10", "r11", "r12", "r13", "r14", "r15", "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"];

    for (var i = 0; i < regs.length; i++) {
      cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
      dataOffset += Process.pointerSize;

      if (i < regs.length - 1) {
        if (regs[i + 1].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x7e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset++;
        } else {
          cw.putMovRegReg("rdi", regs[i + 1]);
        }
      }
    }

    xmmOffset--;
    cw.putPopReg("rdi");
    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    dataOffset += Process.pointerSize;
    cw.putCallAddress(parser);
    cw.putMovNearPtrReg(data.add(dataOffset), "rax");
    dataOffset += Process.pointerSize;
    var regRestoreOffset = dataOffset - Process.pointerSize * 2;

    for (var i = regs.length - 1; i >= 0; i--) {
      var regRestoreOffset = i * Process.pointerSize;
      cw.putMovRegNearPtr("rdi", data.add(regRestoreOffset));

      if (i > 0) {
        if (regs[i].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x6e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset--;
        } else {
          cw.putMovRegReg(regs[i], "rdi");
        }
      }
    }

    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    var rdiBackup = dataOffset;
    dataOffset += Process.pointerSize;
    var cbAddressOffset = rdiBackup - Process.pointerSize;
    cw.putMovRegNearPtr("rdi", data.add(cbAddressOffset));
    cw.putMovNearPtrReg(data.add(dataOffset), "r13");
    var r13Backup = dataOffset;
    cw.putMovRegReg("r13", "rdi");
    cw.putMovRegNearPtr("rdi", data.add(rdiBackup));
    cw.putCallReg("r13");
    cw.putMovRegNearPtr("r13", data.add(r13Backup));
    var retAddressOffset = cbAddressOffset - Process.pointerSize;
    cw.putJmpNearPtr(data.add(retAddressOffset));
    cw.flush();
  });
};

JNIEnvInterceptorX64.prototype.setUpVaListArgExtract = function (vaList) {
  this.grOffset = Memory.readU32(vaList);
  this.grOffsetStart = this.grOffset;
  this.fpOffset = Memory.readU32(vaList.add(4));
  this.fpOffsetStart = this.fpOffset;
  this.overflowPtr = Memory.readPointer(vaList.add(Process.pointerSize));
  this.dataPtr = Memory.readPointer(vaList.add(Process.pointerSize * 2));
};

JNIEnvInterceptorX64.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = NULL;

  if (method.params[paramId] === "float" || method.params[paramId] === "double") {
    if ((this.fpOffset - this.fpOffsetStart) / Process.pointerSize < 14) {
      currentPtr = this.dataPtr.add(this.fpOffset);
      this.fpOffset += Process.pointerSize * 2;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  } else {
    if ((this.grOffset - this.grOffsetStart) / Process.pointerSize < 2) {
      currentPtr = this.dataPtr.add(this.grOffset);
      this.grOffset += Process.pointerSize;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  }

  return currentPtr;
};

JNIEnvInterceptorX64.prototype.resetVaListArgExtract = function () {
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
};

module.exports = JNIEnvInterceptorX64;

},{"../jni_env_interceptor":6}],9:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorX86(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorX86.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorX86.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0x400 + Process.pointerSize;
    cw.putPopReg("eax");
    cw.putMovNearPtrReg(text.add(dataOffset + Process.pointerSize), "eax");
    cw.putCallAddress(parser);
    cw.putCallReg("eax");
    cw.putJmpNearPtr(text.add(dataOffset + Process.pointerSize));
    cw.flush();
  }); // required for some reason...

  Interceptor.attach(text.add(0), function () {});
};

JNIEnvInterceptorX86.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorX86.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "int64") {
    retval = registers.edx.toString().substring(2) + registers.eax.toString().substring(2);
  } else if (retType === "double" || retType === "float") {//TODO - currently does not support floating point returns on x86
  }

  return retval;
};

module.exports = JNIEnvInterceptorX86;

},{"../../utils/types":14,"../jni_env_interceptor":6}],10:[function(require,module,exports){
var Types = require("./utils/types");

var JavaMethod = require("./utils/java_method");

var JNIThreadManager = require("./jni/jni_thread_manager");

var ReferenceManager = require("./utils/reference_manager");

var TraceTransport = require("./transport/trace_transport");

var JNIEnvInterceptorX86 = require("./jni/x86/jni_env_interceptor_x86");

var JNIEnvInterceptorX64 = require("./jni/x64/jni_env_interceptor_x64");

var JNIEnvInterceptorARM = require("./jni/arm/jni_env_interceptor_arm");

var JNIEnvInterceptorARM64 = require("./jni/arm64/jni_env_interceptor_arm64");

var JavaVMInterceptor = require("./jni/java_vm_interceptor");

var threads = new JNIThreadManager();
var references = new ReferenceManager();
var transport = new TraceTransport(threads);
var jniEnvInterceptor = null;

if (Process.arch === "ia32") {
  jniEnvInterceptor = new JNIEnvInterceptorX86(references, threads, transport);
} else if (Process.arch === "x64") {
  jniEnvInterceptor = new JNIEnvInterceptorX64(references, threads, transport);
} else if (Process.arch === "arm") {
  jniEnvInterceptor = new JNIEnvInterceptorARM(references, threads, transport);
} else if (Process.arch === "arm64") {
  jniEnvInterceptor = new JNIEnvInterceptorARM64(references, threads, transport);
}

if (!jniEnvInterceptor) {
  throw new Error(Process.arch + " currently unsupported, please file an issue.");
}

var javaVMInterceptor = new JavaVMInterceptor(references, threads, jniEnvInterceptor);
jniEnvInterceptor.setJavaVMInterceptor(javaVMInterceptor);
var libsToTrack = ['*'];
var trackedLibs = {};
var libBlacklist = {}; // need to run this before start up.

function checkLibrary(path) {
  if (libsToTrack.length === 0) {
    var op = recv('libraries', function (message) {
      libsToTrack = message.payload;
    });
    op.wait();
  }

  if (libsToTrack.length === 1) {
    if (libsToTrack[0] === "*") {
      return true;
    }
  }

  for (var i = 0; i < libsToTrack.length; i++) {
    if (path.indexOf(libsToTrack[i]) > -1) {
      return true;
    }
  }

  return false;
}

function interceptJNIOnLoad(jniOnLoadAddr) {
  return Interceptor.attach(jniOnLoadAddr, {
    onEnter: function (args) {
      var shadowJavaVM = NULL;
      var javaVM = ptr(args[0]);

      if (!threads.hasJavaVM()) {
        threads.setJavaVM(javaVM);
      }

      if (!javaVMInterceptor.isInitialised()) {
        shadowJavaVM = javaVMInterceptor.create();
      } else {
        shadowJavaVM = javaVMInterceptor.get();
      }

      args[0] = shadowJavaVM;
    }
  });
}

function interceptJNIFunction(jniFunctionAddr) {
  return Interceptor.attach(jniFunctionAddr, {
    onEnter: function (args) {
      var shadowJNIEnv = NULL;
      var threadId = this.threadId;
      var jniEnv = ptr(args[0]);
      threads.setJNIEnv(threadId, jniEnv);

      if (!jniEnvInterceptor.isInitialised()) {
        shadowJNIEnv = jniEnvInterceptor.create();
      } else {
        shadowJNIEnv = jniEnvInterceptor.get();
      }

      args[0] = shadowJNIEnv;
    }
  });
}

var dlopenRef = Module.findExportByName(null, "dlopen");
var dlsymRef = Module.findExportByName(null, "dlsym");
var dlcloseRef = Module.findExportByName(null, "dlclose");

if (dlopenRef && dlsymRef && dlcloseRef) {
  var dlopen = new NativeFunction(dlopenRef, 'pointer', ['pointer', 'int']);
  Interceptor.replace(dlopen, new NativeCallback(function (filename, mode) {
    var path = Memory.readCString(filename);
    var retval = dlopen(filename, mode);

    if (checkLibrary(path)) {
      trackedLibs[ptr(retval)] = true;
    } else {
      libBlacklist[ptr(retval)] = true;
    }

    return retval;
  }, 'pointer', ['pointer', 'int']));
  var dlsym = new NativeFunction(dlsymRef, "pointer", ["pointer", "pointer"]);
  Interceptor.attach(dlsym, {
    onEnter: function (args) {
      this.handle = ptr(args[0]);

      if (libBlacklist[this.handle]) {
        return;
      }

      this.symbolAddr = ptr(args[1]);
    },
    onLeave: function (retval) {
      if (retval.isNull() || libBlacklist[this.handle]) {
        return;
      }

      if (!trackedLibs[this.handle]) {
        // Android 7 and above miss the initial dlopen call.
        // Give it another chance in dlsym.
        var mod = Process.findModuleByAddress(retval);

        if (checkLibrary(mod.name)) {
          trackedLibs[this.handle] = true;
        }
      }

      if (trackedLibs[this.handle]) {
        var symbol = Memory.readCString(this.symbolAddr);

        if (symbol === "JNI_OnLoad") {
          interceptJNIOnLoad(ptr(retval));
        } else if (symbol.startsWith("Java_")) {
          interceptJNIFunction(ptr(retval));
        }
      } else {
        var name = libsToTrack[0];

        if (name !== "*") {
          var mod = Process.findModuleByAddress(retval);
          name = mod.name;
        }

        if (libsToTrack.indexOf(name) > -1 || name === "*") {
          interceptJNIFunction(ptr(retval));
        }
      }
    }
  });
  var dlclose = new NativeFunction(dlcloseRef, "int", ["pointer"]);
  Interceptor.attach(dlclose, {
    onEnter: function (args) {
      var handle = ptr(args[0]);

      if (trackedLibs[handle]) {
        this.handle = handle;
      }
    },
    onLeave: function (retval) {
      if (this.handle) {
        if (retval.isNull()) {
          delete trackedLibs[this.handle];
        }
      }
    }
  });
}

if (libsToTrack.length > 0) {
  console.error("Welcome to jnitrace. Tracing is running...");
  console.warn("NOTE: the recommended way to run this module is using the " + "python wrapper. It provides nicely formated coloured output " + "in the form of frida-trace. To get jnitrace run " + "'pip install jnitrace' or go to " + "'https://github.com/chame1eon/jnitrace'");
}

},{"./jni/arm/jni_env_interceptor_arm":3,"./jni/arm64/jni_env_interceptor_arm64":4,"./jni/java_vm_interceptor":5,"./jni/jni_thread_manager":7,"./jni/x64/jni_env_interceptor_x64":8,"./jni/x86/jni_env_interceptor_x86":9,"./transport/trace_transport":11,"./utils/java_method":12,"./utils/reference_manager":13,"./utils/types":14}],11:[function(require,module,exports){
var Types = require("../utils/types");

function TraceTransport(threads) {
  this.threads = threads;
  this.start = Date.now();
} // add - additional method data - will include jtypes for va_list and ...


TraceTransport.prototype.trace = function (method, args, ret, context, add) {
  var threadId = Process.getCurrentThreadId();
  var outputArgs = [];
  var outputRet = NULL;
  var jniEnv = this.threads.getJNIEnv(threadId);
  var sendData = null;
  outputArgs.push({
    value: jniEnv
  });

  if (method.name === "DefineClass") {
    var name = Memory.readCString(args[1]);
    args.push({
      value: args[1],
      data: name
    });
    args.push({
      value: args[2]
    });
    var classData = Memory.readByteArray(args[3], args[4]);
    args.push({
      value: args[3],
      data_for: 3
    });
    sendData = classData;
    args.push({
      value: args[4]
    });
  } else if (method.name === "FindClass") {
    var name = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: name
    });
  } else if (method.name === "ThrowNew") {
    var message = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: message
    });
  } else if (method.name === "FatalError") {
    var message = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: message
    });
  } else if (method.name.endsWith("ID")) {
    var name = Memory.readCString(args[2]);
    var sig = Memory.readCString(args[3]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: name
    });
    outputArgs.push({
      value: args[3],
      data: sig
    });
  } else if (method.name === "NewString") {
    var unicode = Memory.readByteArray(args[1], args[2]);
    outputArgs.push({
      value: args[1],
      data_for: 1
    });
    sendData = unicode;
    outputArgs.push({
      value: args[2]
    });
  } else if (method.name.startsWith("Get") && method.name.endsWith("Chars") || method.name.endsWith("Elements") || method.name.endsWith("ArrayCritical") || method.name === "GetStringCritical") {
    outputArgs.push({
      value: args[1]
    });

    if (!args[2].isNull()) {
      outputArgs.push({
        value: args[2],
        data: Memory.readU32(args[2])
      });
    } else {
      outputArgs.push({
        value: args[2]
      });
    }

    if (args.length > 3) {
      outputArgs.push({
        value: args[3]
      });
    }
  } else if (method.name.startsWith("Release") && method.name.endsWith("Chars")) {
    var unicode = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: unicode
    });
  } else if (method.name.endsWith("Region")) {
    var type = method.args[4].substring(0, method.args[4].length - 1);
    var nType = Types.convertNativeJTypeToFridaType(type);
    var size = Types.sizeOf(nType);
    var region = Memory.readByteArray(args[4], args[3] * size);

    for (var i = 1; i < args.length - 1; i++) {
      outputArgs.push({
        value: args[i]
      });
    }

    outputArgs.push({
      value: args[args.length - 1],
      data_for: args.length - 1
    });
    sendData = region;
  } else if (method.name === "NewStringUTF") {
    var utf = Memory.readUtf8String(args[1]);
    outputArgs.push({
      value: args[1],
      data: utf
    });
  } else if (method.name === "RegisterNatives") {
    outputArgs.push({
      value: args[1]
    });
    var size = args[3];
    var data = [];

    for (var i = 0; i < size * 3; i += 3) {
      var namePtr = Memory.readPointer(args[2].add(i * Process.pointerSize));
      var name = Memory.readCString(namePtr);
      var sigPtr = Memory.readPointer(args[2].add((i + 1) * Process.pointerSize));
      var sig = Memory.readCString(sigPtr);
      var addr = Memory.readPointer(args[2].add((i + 2) * Process.pointerSize));
      data.push({
        name: {
          value: namePtr,
          data: name
        },
        sig: {
          value: sigPtr,
          data: sig
        },
        addr: {
          value: addr
        }
      });
    }

    outputArgs.push({
      value: args[2],
      data: data
    });
    outputArgs.push({
      value: args[3]
    });
  } else if (method.name === "GetJavaVM") {
    outputArgs.push({
      value: args[1],
      data: Memory.readPointer(args[1])
    });
  } else if (method.name === "ReleaseStringCritical") {
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: Memory.readCString(args[2])
    });
  } else {
    for (var i = 1; i < args.length; i++) {
      outputArgs.push({
        value: args[i]
      });
    }
  }

  outputRet = ret;
  var backtrace = []; // verify that a backtrace is possible.
  // sometimes the NativeCallback provides erroneous CpuContexts

  if (context && Process.findModuleByAddress(context.pc) && Process.findRangeByAddress(context.sp)) {
    var bt = Thread.backtrace(context, Backtracer.FUZZY);

    for (var i = 0; i < bt.length; i++) {
      backtrace.push({
        address: bt[i],
        module: Process.findModuleByAddress(bt[i])
      });
    }
  }

  send({
    method: method,
    args: outputArgs,
    ret: outputRet,
    threadId: Process.getCurrentThreadId(),
    backtrace: backtrace,
    timestamp: Date.now() - this.start,
    additional_params: add
  }, sendData);
};

module.exports = TraceTransport;

},{"../utils/types":14}],12:[function(require,module,exports){
function JavaMethod(signature) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z", "V"];
  var isArray = false;
  var isRet = false;
  var jParamTypes = [];
  var jRetType = null;

  for (var i = 0; i < signature.length; i++) {
    if (signature.charAt(i) === "(") {
      continue;
    }

    if (signature.charAt(i) === ")") {
      isRet = true;
      continue;
    }

    if (signature.charAt(i) === "[") {
      isArray = true;
      continue;
    }

    var jtype = null;

    if (primitiveTypes.indexOf(signature.charAt(i)) > -1) {
      jtype = signature.charAt(i);
    } else if (signature.charAt(i) === "L") {
      var end = signature.indexOf(";", i) + 1;
      jtype = signature.substring(i, end);
      i = end - 1;
    } //TODO DELETE


    if (isArray) {
      jtype = "[" + jtype;
    }

    if (!isRet) {
      jParamTypes.push(jtype);
    } else {
      jRetType = jtype;
    }

    isArray = false;
  }

  this.signature = signature;
  this.params = jParamTypes;
  this.ret = jRetType;
}

JavaMethod.prototype.getParams = function () {
  return this.params;
};

JavaMethod.prototype.getRet = function () {
  return this.ret;
};

module.exports = JavaMethod;

},{}],13:[function(require,module,exports){
function ReferenceManager() {
  this.references = {};
}

ReferenceManager.prototype.add = function (ref) {
  this.references[ref] = ref;
};

ReferenceManager.prototype.release = function (ref) {
  if (this.references[ref]) {
    delete this.references[ref];
  }
};

module.exports = ReferenceManager;

},{}],14:[function(require,module,exports){
function Types() {}

Types.sizeOf = function (type) {
  if (type === "double" || type === "float" || type === "int64") {
    return 8;
  } else if (type === "char") {
    return 1;
  } else {
    return Process.pointerSize;
  }
};

Types.convertNativeJTypeToFridaType = function (jtype) {
  if (jtype.indexOf("*") > -1) {
    return "pointer";
  }

  if (jtype === "jmethodID") {
    return "pointer";
  }

  if (jtype === "jfieldID") {
    return "pointer";
  }

  if (jtype === "va_list") {
    return "va_list";
  }

  if (jtype === "jweak") {
    jtype = "jobject";
  }

  if (jtype === "jthrowable") {
    jtype = "jobject";
  }

  if (jtype.indexOf("Array") > -1) {
    jtype = "jarray";
  }

  if (jtype === "jarray") {
    jtype = "jobject";
  }

  if (jtype === "jstring") {
    jtype = "jobject";
  }

  if (jtype === "jclass") {
    jtype = "jobject";
  }

  if (jtype === "jobject") {
    return "pointer";
  }

  if (jtype === "jsize") {
    jtype = "jint";
  }

  if (jtype === "jdouble") {
    return "double";
  }

  if (jtype === "jfloat") {
    return "float";
  }

  if (jtype === "jchar") {
    return "uint16";
  }

  if (jtype === "jboolean") {
    return "char";
  }

  if (jtype === "jlong") {
    return "int64";
  }

  if (jtype === "jint") {
    return "int";
  }

  if (jtype === "jshort") {
    return "int16";
  }

  if (jtype === "jbyte") {
    return "char";
  }

  return jtype;
};

Types.convertJTypeToNativeJType = function (jtype, isArray) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z"];
  var result = "";

  if (jtype === "B") {
    result += "jbyte";
  } else if (jtype === "S") {
    result += "jshort";
  } else if (jtype === "I") {
    result += "jint";
  } else if (jtype === "J") {
    result += "jlong";
  } else if (jtype === "F") {
    result += "jfloat";
  } else if (jtype === "D") {
    result += "jdouble";
  } else if (jtype === "C") {
    result += "jchar";
  } else if (jtype === "Z") {
    result += "jboolean";
  } else if (jtype.charAt(0) === "L") {
    if (jtype === "Ljava/lang/String;") {
      result += "jstring";
    } else if (jtype === "Ljava/lang/Class;") {
      result += "jclass";
    } else {
      result += "jobject";
    }
  }

  if (isArray) {
    if (result === "jstring") {
      result = "jobject";
    }

    result += "Array";
  }

  return result;
};

module.exports = Types;

},{}]},{},[10])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy5udm0vdmVyc2lvbnMvbm9kZS92MTIuNy4wL2xpYi9ub2RlX21vZHVsZXMvZnJpZGEtY29tcGlsZS9ub2RlX21vZHVsZXMvYnJvd3Nlci1wYWNrL19wcmVsdWRlLmpzIiwiZGF0YS9qYXZhX3ZtLmpzb24iLCJkYXRhL2puaV9lbnYuanNvbiIsImpuaS9hcm0vam5pX2Vudl9pbnRlcmNlcHRvcl9hcm0uanMiLCJqbmkvYXJtNjQvam5pX2Vudl9pbnRlcmNlcHRvcl9hcm02NC5qcyIsImpuaS9qYXZhX3ZtX2ludGVyY2VwdG9yLmpzIiwiam5pL2puaV9lbnZfaW50ZXJjZXB0b3IuanMiLCJqbmkvam5pX3RocmVhZF9tYW5hZ2VyLmpzIiwiam5pL3g2NC9qbmlfZW52X2ludGVyY2VwdG9yX3g2NC5qcyIsImpuaS94ODYvam5pX2Vudl9pbnRlcmNlcHRvcl94ODYuanMiLCJtYWluLmpzIiwidHJhbnNwb3J0L3RyYWNlX3RyYW5zcG9ydC5qcyIsInV0aWxzL2phdmFfbWV0aG9kLmpzIiwidXRpbHMvcmVmZXJlbmNlX21hbmFnZXIuanMiLCJ1dGlscy90eXBlcy5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDMURBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNB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a0MsVUFBUyxLQUFULEVBQWdCLE9BQWhCLEVBQXlCO0FBQ3pELE1BQUksY0FBYyxHQUFHLENBQUMsR0FBRCxFQUFNLEdBQU4sRUFBVyxHQUFYLEVBQWdCLEdBQWhCLEVBQXFCLEdBQXJCLEVBQTBCLEdBQTFCLEVBQStCLEdBQS9CLEVBQW9DLEdBQXBDLENBQXJCO0FBQ0EsTUFBSSxNQUFNLEdBQUcsRUFBYjs7QUFFQSxNQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ2pCLElBQUEsTUFBTSxJQUFJLE9BQVY7QUFDRCxHQUZELE1BRU8sSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxRQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksTUFBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLE9BQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxRQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksU0FBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLE9BQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxVQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxDQUFDLE1BQU4sQ0FBYSxDQUFiLE1BQW9CLEdBQXhCLEVBQTZCO0FBQ2xDLFFBQUksS0FBSyxLQUFLLG9CQUFkLEVBQW9DO0FBQ2xDLE1BQUEsTUFBTSxJQUFJLFNBQVY7QUFDRCxLQUZELE1BRU8sSUFBRyxLQUFLLEtBQUssbUJBQWIsRUFBa0M7QUFDdkMsTUFBQSxNQUFNLElBQUksUUFBVjtBQUNELEtBRk0sTUFFQTtBQUNMLE1BQUEsTUFBTSxJQUFJLFNBQVY7QUFDRDtBQUNGOztBQUVELE1BQUksT0FBSixFQUFhO0FBQ1gsUUFBSSxNQUFNLEtBQUssU0FBZixFQUEwQjtBQUN4QixNQUFBLE1BQU0sR0FBRyxTQUFUO0FBQ0Q7O0FBQ0QsSUFBQSxNQUFNLElBQUksT0FBVjtBQUNEOztBQUVELFNBQU8sTUFBUDtBQUNELENBdENEOztBQXdDQSxNQUFNLENBQUMsT0FBUCxHQUFpQixLQUFqQiIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIn0=
