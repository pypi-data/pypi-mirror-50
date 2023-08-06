#ifndef COCONET_CPPBIND_COCONET_H_
#define COCONET_CPPBIND_COCONET_H_

#include <memory>
#include <coconet/runtime/singleton.h>
#include <coconet/autograd/executor.h>
#include <coconet/autograd/variable.h>
#include <coconet/autograd/function.h>


namespace coconet
{
	namespace cppbind
	{
		template<class T, PlatformType Platform = PlatformType::CPU>
		class TensorFactory
		{
		public:
			static std::shared_ptr<autograd::Variable<T, Platform>> zeros(tensor::DimVector dimensions);
			static std::shared_ptr<autograd::Variable<T, Platform>> ones(tensor::DimVector dimensions);
		};


		template<class T, PlatformType Platform>
		inline std::shared_ptr<autograd::Variable<T, Platform>> TensorFactory<T, Platform>::zeros(tensor::DimVector dimensions)
		{
			auto session = runtime::Singleton<autograd::VariableGraph>::getInstance();

			auto ret = std::make_shared<autograd::Variable<T, Platform>>(dimensions);
			ret->fill_(0);

			session.add_variable(ret);
			return ret;
		}

		template<class T, PlatformType Platform>
		inline std::shared_ptr<autograd::Variable<T, Platform>> TensorFactory<T, Platform>::ones(tensor::DimVector dimensions)
		{
			auto session = runtime::Singleton<autograd::VariableGraph>::getInstance();

			auto ret = std::make_shared<autograd::Variable<T, Platform>>(dimensions);
			ret->fill_(1);
			
			session.add_variable(ret);
			return ret;
		}

		template<class T, PlatformType Platform>
		std::shared_ptr<autograd::Variable<T, Platform>> add(std::shared_ptr<autograd::Variable<T, Platform>> lhs, std::shared_ptr<autograd::Variable<T, Platform>> rhs)
		{
			auto session = runtime::Singleton<autograd::VariableGraph>::getInstance();

			auto addOp = std::make_shared<coconet::autograd::AddFunction>();
			auto ret = addOp->forward({ lhs,rhs })[0];
			session.add_edge({ lhs, rhs }, { ret }, addOp);
			return std::dynamic_pointer_cast<autograd::Variable<T, Platform>>(ret);
		}
	}

}


#endif // !COCONET_CPPBIND_COCONET_H_
