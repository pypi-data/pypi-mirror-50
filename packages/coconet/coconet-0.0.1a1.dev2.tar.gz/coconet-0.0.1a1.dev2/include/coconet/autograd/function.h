#ifndef COCONET_AUTOGRAD_FUNCTION_H_
#define COCONET_AUTOGRAD_FUNCTION_H_

#include <memory>

#include <coconet/autograd/variable.h>

namespace coconet
{
	namespace autograd
	{
		class FunctionContext
		{
		private:
			std::vector<tensor::ITensor*> _saved_tensors;
		public:
			void save(tensor::ITensor* tensor)
			{
				_saved_tensors.push_back(tensor);
			}

			std::vector<tensor::ITensor*> get_saved_tensors() const
			{
				return _saved_tensors;
			}
		};

		class FunctionBase
		{
		public:
			FunctionContext context;

			// info
			virtual std::int32_t num_inputs() const = 0;
			virtual std::int32_t num_outputs() const = 0;

			// forward and backward
			virtual std::vector<std::shared_ptr<IVariable>> forward(std::vector<std::shared_ptr<IVariable>> inputs) = 0;
			virtual std::vector<std::shared_ptr<IVariable>> backward(std::vector<std::shared_ptr<IVariable>> output_grad) = 0;
		};

		class MatmulFunction : public FunctionBase
		{
		public:
			virtual std::int32_t num_inputs() const override { return 2; }
			virtual std::int32_t num_outputs() const override { return 1; }
			virtual std::vector<std::shared_ptr<IVariable>> forward(std::vector<std::shared_ptr<IVariable>> inputs) override
			{
				return {};
			}

			virtual std::vector<std::shared_ptr<IVariable >> backward(std::vector<std::shared_ptr<IVariable>> output_grad) override
			{
				return {};
			}
		};

		class AddFunction :public FunctionBase
		{
		public:
			virtual std::int32_t num_inputs() const override { return 2; }
			virtual std::int32_t num_outputs() const override { return 1; }
			virtual std::vector<std::shared_ptr<IVariable>> forward(std::vector<std::shared_ptr<IVariable>> inputs) override
			{
				return {};
			}

			virtual std::vector<std::shared_ptr<IVariable>> backward(std::vector<std::shared_ptr<IVariable>> output_grad) override
			{
				return {};
			}
		};
		
	}


}

#endif // !COCONET_AUTOGRAD_FUNCTION_H_
