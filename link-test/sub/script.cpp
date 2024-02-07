#include <iostream>
#include <Windows.h>

#if not defined DYNAMIC_LINK
extern void use_engine();
#endif

#if defined DYNAMIC_LINK
extern "C" __declspec(dllexport)
#endif
void call_script() {
    std::cout << "Calling script" << std::endl;
    #if defined DYNAMIC_LINK
    auto lib = LoadLibraryA("main.exe");
    if (lib) {
        auto use_engine = (void(*)())GetProcAddress(lib, "use_engine");
        if (use_engine) {
            #endif
            use_engine();
            #if defined DYNAMIC_LINK
        }
        FreeLibrary(lib);
    }
    #endif
}