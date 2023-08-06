#ifndef COCONET_RUNTIME_SINGLETON_H_
#define COCONET_RUNTIME_SINGLETON_H_

#include <thread>
#include <mutex>

namespace coconet
{
    namespace runtime
    {
        template<class T>
        class Singleton
        {
        public:
            static T& getInstance()
            {
                static std::once_flag oc;
                std::call_once(oc,[&]{value=new T();});
                return *value;
            }
        private:
            static T* value;
        };
        
        template<class T>
        T * Singleton<T>::value(nullptr);
    }
}

#endif