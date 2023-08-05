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
        "ret": "jboolean*"
    },
    {
        "name": "GetByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jboolean*"
        ],
        "ret": "jbyte*"
    },
    {
        "name": "GetCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jboolean*"
        ],
        "ret": "jchar*"
    },
    {
        "name": "GetShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jboolean*"
        ],
        "ret": "jshort*"
    },
    {
        "name": "GetIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jboolean*"
        ],
        "ret": "jint*"
    },
    {
        "name": "GetLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jboolean*"
        ],
        "ret": "jlong*"
    },
    {
        "name": "GetFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jboolean*"
        ],
        "ret": "jfloat*"
    },
    {
        "name": "GetDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jboolean*"
        ],
        "ret": "jdouble*"
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

JNIEnvInterceptorARM.prototype.createStubFunction = function () {
  var stub = Memory.alloc(Process.pageSize);
  Memory.patchCode(stub, Process.pageSize, function (code) {
    var cw = new ArmWriter(code, {
      pc: stub
    });
    cw.putInstruction(0xe52de004);
    cw.putInstruction(0xe49df004);
  });
  return stub;
};

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
  });
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

JNIEnvInterceptorARM64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM64.prototype.createStubFunction = function () {
  var stub = Memory.alloc(Process.pageSize);
  Memory.patchCode(stub, Process.pageSize, function (code) {
    var cw = new Arm64Writer(code, {
      pc: stub
    });
    cw.putInstruction(0xd65f03c0);
  });
  return stub;
};

JNIEnvInterceptorARM64.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  //text = Memory.alloc(Process.pageSize);
  Memory.writePointer(text.add(0x400), parser);
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
  });
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

    self.transport.trace(method, localArgs, ret, this.context, add);

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
  var vaArgsBts = {};
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
      self.transport.trace(method, localArgs, ret, vaArgsBts[this.threadId], vaArgs.javaParams);
      delete vaArgsBts[this.threadId];
      return ret;
    }, retType, callbackParams);
    self.references.add(mainCallback);
    self.fastMethodLookup[methodId] = mainCallback;
    return mainCallback;
  }, "pointer", ["pointer", "pointer", "pointer"]);
  this.references.add(vaArgsCallback);
  self.buildVaArgParserShellcode(text, data, vaArgsCallback);
  Interceptor.attach(text, function (args) {
    vaArgsBts[this.threadId] = Thread.backtrace(this.context, Backtracer.FUZZY);
  });
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
        this.enterCtx = this.context;
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
        self.transport.trace(methodData, this.args, ret, this.enterCtx, add);
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

JNIEnvInterceptor.prototype.createStubFunction = function () {
  return new NativeCallback(function () {}, 'void', []);
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
      var trampoline = this.createStubFunction();
      this.references.add(trampoline); // ensure the CpuContext will be populated

      Interceptor.replace(trampoline, callback);
      Memory.writePointer(newJNIEnvStruct.add(offset), trampoline);
    } else if (method.args[method.args.length - 1] === "va_list") {
      var callback = this.createJNIVaListIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else {
      var callback = this.createJNIIntercept(i, methodAddr);
      var trampoline = this.createStubFunction();
      this.references.add(trampoline); // ensure the CpuContext will be populated

      Interceptor.replace(trampoline, callback);
      Memory.writePointer(newJNIEnvStruct.add(offset), trampoline);
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
  });
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
  var backtrace = [];

  if (context) {
    var bt = context;

    if (!(bt instanceof Array)) {
      bt = Thread.backtrace(context, Backtracer.FUZZY);
    }

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

Types.convertJTypeToNativeJType = function (jtype) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z"];
  var result = "";
  var isArray = false;

  if (jtype.startsWith("[")) {
    isArray = true;
    jtype = jtype.substring(1);
  }

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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uLy4uLy5udm0vdmVyc2lvbnMvbm9kZS92MTIuNy4wL2xpYi9ub2RlX21vZHVsZXMvZnJpZGEtY29tcGlsZS9ub2RlX21vZHVsZXMvYnJvd3Nlci1wYWNrL19wcmVsdWRlLmpzIiwiZGF0YS9qYXZhX3ZtLmpzb24iLCJkYXRhL2puaV9lbnYuanNvbiIsImpuaS9hcm0vam5pX2Vudl9pbnRlcmNlcHRvcl9hcm0uanMiLCJqbmkvYXJtNjQvam5pX2Vudl9pbnRlcmNlcHRvcl9hcm02NC5qcyIsImpuaS9qYXZhX3ZtX2ludGVyY2VwdG9yLmpzIiwiam5pL2puaV9lbnZfaW50ZXJjZXB0b3IuanMiLCJqbmkvam5pX3RocmVhZF9tYW5hZ2VyLmpzIiwiam5pL3g2NC9qbmlfZW52X2ludGVyY2VwdG9yX3g2NC5qcyIsImpuaS94ODYvam5pX2Vudl9pbnRlcmNlcHRvcl94ODYuanMiLCJtYWluLmpzIiwidHJhbnNwb3J0L3RyYWNlX3RyYW5zcG9ydC5qcyIsInV0aWxzL2phdmFfbWV0aG9kLmpzIiwidXRpbHMvcmVmZXJlbmNlX21hbmFnZXIuanMiLCJ1dGlscy90eXBlcy5qcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDMURBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNB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QW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLFVBQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLENBQUMsTUFBTixDQUFhLENBQWIsTUFBb0IsR0FBeEIsRUFBNkI7QUFDbEMsUUFBSSxLQUFLLEtBQUssb0JBQWQsRUFBb0M7QUFDbEMsTUFBQSxNQUFNLElBQUksU0FBVjtBQUNELEtBRkQsTUFFTyxJQUFHLEtBQUssS0FBSyxtQkFBYixFQUFrQztBQUN2QyxNQUFBLE1BQU0sSUFBSSxRQUFWO0FBQ0QsS0FGTSxNQUVBO0FBQ0wsTUFBQSxNQUFNLElBQUksU0FBVjtBQUNEO0FBQ0Y7O0FBRUQsTUFBSSxPQUFKLEVBQWE7QUFDWCxRQUFJLE1BQU0sS0FBSyxTQUFmLEVBQTBCO0FBQ3hCLE1BQUEsTUFBTSxHQUFHLFNBQVQ7QUFDRDs7QUFDRCxJQUFBLE1BQU0sSUFBSSxPQUFWO0FBQ0Q7O0FBRUQsU0FBTyxNQUFQO0FBQ0QsQ0E1Q0Q7O0FBOENBLE1BQU0sQ0FBQyxPQUFQLEdBQWlCLEtBQWpCIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIifQ==
