#ifndef COCONET_COTENSOR_STORAGE_H_
#define COCONET_COTENSOR_STORAGE_H_

#include <memory>
#include <coconet/tensor/storage.h>
#include <coconet/cotensor/allocator.h>

namespace coconet
{
	namespace cotensor
	{
		class CoTensorStorage: public tensor::Storage
		{
		private:
			char* _data;
			idx_type _len;
			DataType _dtype;
			std::unique_ptr<tensor::Allocator> _allocator;
		public:
			CoTensorStorage();
			CoTensorStorage(DataType data_type, idx_type size = 0);
			CoTensorStorage(const CoTensorStorage& other);
			CoTensorStorage(CoTensorStorage&& other);
			~CoTensorStorage();
			CoTensorStorage& operator= (const CoTensorStorage& other);
			CoTensorStorage& operator= (CoTensorStorage&& other);
			
			
			void swap(CoTensorStorage& other) noexcept;

			// convert
			virtual void to_byte() override;
			virtual void to_char() override;
			virtual void to_short() override;
			virtual void to_int() override;
			virtual void to_long() override;
			virtual void to_float() override;
			virtual void to_double() override;

			// info
			virtual char* data_ptr() noexcept override;
			virtual const char* data_ptr() const noexcept override;
			virtual DataType dtype() const override;
			virtual std::int32_t element_size() const override;
			virtual PlatformType platform() const override;
			virtual idx_type size() const override;
			virtual idx_type numel() const override;

			// manipulate
			virtual void resize_(idx_type n) override;
		};
	}
}


#endif //!COCONET_COTENSOR_STORAGE_H_