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

    template <typename T>
    class TempClass{
        private:
        void print(){
            std::cout << "TempClass" << std::endl;
        }
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
        void SOmeMethod()
        {
            std::cout << "HogeComponent::SOmeMethod" << std::endl;
        }

        private:
        void privateMethod()
        {
            std::cout << "HogeComponent::privateMethod" << std::endl;
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

using tempint = TestFlamework::TempClass<int> ;

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
    auto some = std::shared_ptr<TestFlamework::TempClass<int>>();
    TestFlamework::TempClass<int> temp;
    std::this_thread::sleep_for(std::chrono::seconds(1));
}