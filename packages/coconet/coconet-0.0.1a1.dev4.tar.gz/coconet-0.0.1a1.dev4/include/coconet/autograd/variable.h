#ifndef COCONET_AUTOGRAD_VARIABLE_H_
#define COCONET_AUTOGRAD_VARIABLE_H_

#include <memory>
#include <string>
#include <stdexcept>
#include <initializer_list>

#include <coconet/core/type.h>
#include <coconet/tensor/tensor.h>
#include <coconet/tensor/index.h>
#include <coconet/cotensor/tensor.h>
#include <coconet/cotensor/apply.h>

namespace coconet
{
	namespace autograd
	{
		class IVariable: public std::enable_shared_from_this<IVariable>
		{
		public:
			virtual void fill_(scalar_type value) = 0;
			virtual std::string to_string() const = 0;
		};

		template<class T, PlatformType Platform = PlatformType::CPU>
		class Variable : public IVariable
		{
		public:

		private:
			/*
			std::unique_ptr<cotensor::CoTensor<T>> _data;
			std::unique_ptr<cotensor::CoTensor<f32>> _grad;
			std::unique_ptr<OpBase> _grad_fn;
			std::vector<IVariable*> _inputs;
			*/
		};

		template<class T>
		class Variable<T, PlatformType::CPU> : public IVariable
		{
		public:
			using value_type = T;
			using self_type = Variable<T, PlatformType::CPU>;
			using base_type = IVariable;

			using raw_pointer = self_type * ;
			using raw_const_pointer = const self_type*;
			using shared_pointer = std::shared_ptr<self_type>;
			using reference = self_type & ;
			using const_reference = const self_type&;
		public:
			Variable(const tensor::DimVector& dimensions);

		public:
			// create
			static std::shared_ptr<Variable<T, PlatformType::CPU>> zeros(std::initializer_list<idx_type> list);
			static std::shared_ptr<Variable<T, PlatformType::CPU>> ones(std::initializer_list<idx_type> list);
			
			// op
			virtual void fill_(scalar_type value) override;

			// tools
			virtual std::string to_string() const override;
		private:
			std::unique_ptr<cotensor::CoTensor<T>> _data;
			std::unique_ptr<cotensor::CoTensor<f32>> _grad;
		};
		
		template class Variable<f32, PlatformType::CPU>;
		template class Variable<f64, PlatformType::CPU>;
		template class Variable<i8, PlatformType::CPU>;
		template class Variable<i16, PlatformType::CPU>;
		template class Variable<i32, PlatformType::CPU>;
		template class Variable<i64, PlatformType::CPU>;
		template class Variable<u8, PlatformType::CPU>;

		using FloatVariable = Variable<f32, PlatformType::CPU>;
		using DoubleVariable = Variable<f64, PlatformType::CPU>;
		using CharVariable = Variable<i8, PlatformType::CPU>;
		using ShortVariable = Variable<i16, PlatformType::CPU>;
		using IntVariable = Variable<i32, PlatformType::CPU>;
		using LongVariable = Variable<i64, PlatformType::CPU>;
		using ByteVariable = Variable<u8, PlatformType::CPU>;

		template<class T>
		inline Variable<T, PlatformType::CPU>::Variable(const tensor::DimVector& dimensions)
			:_data(new cotensor::CoTensor<T>(dimensions)), _grad(nullptr)
		{
		}

		template<class T>
		inline std::shared_ptr<Variable<T, PlatformType::CPU>> Variable<T, PlatformType::CPU>::zeros(std::initializer_list<idx_type> list)
		{
			std::shared_ptr<Variable<T, PlatformType::CPU>> ret(new Variable<T, PlatformType::CPU>(list));
			ret->fill_(static_cast<T>(0));
			return ret;
		}

		template<class T>
		inline std::shared_ptr<Variable<T, PlatformType::CPU>> Variable<T, PlatformType::CPU>::ones(std::initializer_list<idx_type> list)
		{
			std::shared_ptr<Variable<T, PlatformType::CPU>> ret(new Variable<T, PlatformType::CPU>(list));
			ret->fill_(static_cast<T>(1));
			return ret;
		}

		template<class T>
		inline void Variable<T, PlatformType::CPU>::fill_(scalar_type value)
		{
			cotensor::fill_(*_data, ScalarTo<T>::to(value));
		}

		template<class T>
		inline std::string Variable<T, PlatformType::CPU>::to_string() const
		{
			std::string ret;
			if (_data)
				ret = _data->to_string();
			return ret;
		}

		inline std::shared_ptr<autograd::IVariable> create_variable(const tensor::DimVector& dimensions, coconet::DataType dtype, coconet::PlatformType platform)
		{
			auto ret = std::shared_ptr<autograd::IVariable>(nullptr);
			if (platform == coconet::PlatformType::CPU)
			{
				if (dtype == coconet::DataType::BYTE)
				{
					ret = std::make_shared<autograd::Variable<coconet::u8, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::CHAR)
				{
					ret = std::make_shared<autograd::Variable<coconet::i8, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::SHORT)
				{
					ret = std::make_shared<autograd::Variable<coconet::i16, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::INT)
				{
					ret = std::make_shared<autograd::Variable<coconet::i32, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::LONG)
				{
					ret = std::make_shared<autograd::Variable<coconet::i64, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::FLOAT)
				{
					ret = std::make_shared<autograd::Variable<coconet::f32, coconet::PlatformType::CPU>>(dimensions);
				}
				else if (dtype == coconet::DataType::DOUBLE)
				{
					ret = std::make_shared<autograd::Variable<coconet::f64, coconet::PlatformType::CPU>>(dimensions);
				}
				else
				{
					throw std::runtime_error("Unsupported dtype");
				}
			}
			else
			{
				throw std::runtime_error("Unsupported platform");
			}
			return ret;
		}
	}
}

#endif // !COCONET_AUTOGRAD_VARIABLE_H_
