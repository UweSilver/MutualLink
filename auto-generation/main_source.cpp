#include <iostream>
#include <memory>
#include <chrono>
#include <thread>

namespace TestFlamework
{
    class ExportClass
    {
    public:
        ExportClass()
        {
            refCount = 0;
        }

        void addRef()
        {
            refCount++;
        }
        void removeRef()
        {
            refCount--;
            if (refCount <= 0)
            {
                delete this;
            }
        }

    protected:
        virtual ~ExportClass() = default;

    private:
        unsigned int refCount;
    };

    class HogeComponent : public ExportClass
    {
    public:
        HogeComponent()
        {
            std::cout << "HogeComponent constructor" << std::endl;
        }
        ~HogeComponent()
        {
            std::cout << "HogeComponent destructor" << std::endl;
        }
    };

    class FugaComponent : public ExportClass
    {
    public:
        FugaComponent()
        {
            std::cout << "FugaComponent constructor" << std::endl;
        }
        ~FugaComponent()
        {
            std::cout << "FugaComponent destructor" << std::endl;
        }
    };
}

std::shared_ptr<TestFlamework::HogeComponent> ptr;
int main()
{
    std::cout << "hello, world!" << std::endl;
    {

        auto raw = new TestFlamework::HogeComponent();
        auto hoge = std::shared_ptr<TestFlamework::HogeComponent>(raw, [&](TestFlamework::HogeComponent *ptr)
                                                                  { ptr->removeRef(); });
        hoge->addRef();
        ptr = hoge;
    }
    std::this_thread::sleep_for(std::chrono::seconds(1));
}