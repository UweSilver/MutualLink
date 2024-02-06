#include <Windows.h>
#include <iostream>

#if not defined DYNAMIC_LINK
extern void call_script();
#endif

int main() {
    std::cout << "Hello, World!" << std::endl;
#if defined DYNAMIC_LINK
    auto lib = LoadLibraryA("script.dll");
    if (lib) {
        auto call_script = (void(*)())GetProcAddress(lib, "call_script");
        if (call_script) {
#endif
            call_script();
#if defined DYNAMIC_LINK
        }
        FreeLibrary(lib);
    }
#endif
    return 0;
}
#if defined DYNAMIC_LINK
extern "C" __declspec(dllexport) 
#endif
void use_engine() {
    std::cout << "Using engine" << std::endl;
}