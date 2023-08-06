#ifndef COCONET_COTENSOR_TENSOR_H_
#define COCONET_COTENSOR_TENSOR_H_

#include <string>
#include <memory>
#include <stdexcept>
#include <functional>

#include <coconet/core/type.h>
#include <coconet/tensor/tensor.h>
#include <coconet/tensor/index.h>

#include <coconet/cotensor/storage.h>

namespace coconet
{
	namespace cotensor
	{
		template<class T>
		class CoTensor: public tensor::ITensor
		{
		public:
			using value_type = T;
			using self_type = CoTensor<T>;
			using base_type = ITensor;

			using raw_pointer = self_type * ;
			using raw_const_pointer = const self_type*;
			using shared_pointer = std::shared_ptr<self_type>;
			using reference = self_type & ;
			using const_reference = const self_type&;
		private:
			std::shared_ptr<CoTensorStorage> _rep;
			tensor::DimVector _dimensions;
			tensor::StrideVector _strides;
			idx_type _offset;
			DataType _dtype;
		public:
			CoTensor();
			explicit CoTensor(const tensor::DimVector& dimensions);
			// deprecated
			explicit CoTensor(const tensor::DimVector& dimensions, const tensor::StrideVector& strides);

			CoTensor(const CoTensor& other) = delete;
			CoTensor(CoTensor&& other) = delete;
			CoTensor& operator= (const CoTensor& other) = delete;
			CoTensor& operator= (CoTensor&& other) = delete;

		public:
			T* data_ptr();
			const T* data_ptr() const;
			device_id device();
			DataType dtype() const;
			bool equal(const tensor::ITensor& other) const;
			bool is_contiguous() const;

			idx_type ndimension() const;
			idx_type numel() const;
			idx_type offset() const;
			PlatformType platform() const;
			tensor::DimVector size() const;
			idx_type size(idx_type i) const;
			tensor::Storage& storage();
			tensor::StrideVector stride() const;
			idx_type stride(idx_type i) const;
			std::string to_string() const;
		};

		template class CoTensor<f32>;
		template class CoTensor<f64>;
		template class CoTensor<i8>;
		template class CoTensor<i16>;
		template class CoTensor<i32>;
		template class CoTensor<i64>;
		template class CoTensor<u8>;

		using FloatCoTensor = CoTensor<f32>;
		using DoubleCoTensor = CoTensor<f64>;
		using CharCoTensor = CoTensor<i8>;
		using ShortCoTensor = CoTensor<i16>;
		using IntCoTensor = CoTensor<i32>;
		using LongCoTensor = CoTensor<i64>;
		using ByteCoTensor = CoTensor<u8>;

		template<class T>
		inline CoTensor<T>::CoTensor()
		{
		}

		template<class T>
		inline CoTensor<T>::CoTensor(const tensor::DimVector & dimensions)
			: _rep(nullptr), _dimensions(dimensions), _strides(dimensions.size(), 0), _offset(0), _dtype(GetDataType<T>::get())
		{
			idx_type cum_stride = 1;
			for (idx_type i = static_cast<idx_type>(_strides.size() - 1); i >=0; --i)
			{
				_strides[i] = cum_stride;
				cum_stride *= _dimensions[i];
			}

			_rep = std::make_shared<CoTensorStorage>(_dtype, cum_stride);
		}

		template<class T>
		inline CoTensor<T>::CoTensor(const tensor::DimVector & dimensions, const tensor::StrideVector & strides)
			: _rep(nullptr), _dimensions(dimensions), _strides(strides), _offset(0), _dtype(GetDataType<T>::get())
		{
		}
		template<class T>
		inline T * CoTensor<T>::data_ptr()
		{
			return reinterpret_cast<T*>(_rep->data_ptr()) + _offset;
		}
		template<class T>
		inline const T * CoTensor<T>::data_ptr() const
		{
			return reinterpret_cast<T*>(_rep->data_ptr()) + _offset;
		}
		template<class T>
		inline device_id CoTensor<T>::device()
		{
			return 0;
		}
		template<class T>
		inline DataType CoTensor<T>::dtype() const
		{
			return GetDataType<T>::get();
		}

		template<class T>
		inline bool CoTensor<T>::equal(const tensor::ITensor & other) const
		{
			return false;
		}

		/*
		Returns True if self tensor is contiguous in memory in C order.
		*/
		template<class T>
		inline bool CoTensor<T>::is_contiguous() const
		{
			if (stride(-1) != 1)
				return false;

			for (idx_type i = ndimension() - 1; i > 0; --i)
			{
				if (size(i) * stride(i) != stride(i - 1))
					return false;
			}

			return true;
		}

		template<class T>
		inline idx_type CoTensor<T>::ndimension() const
		{
			return static_cast<idx_type>(_dimensions.size());
		}
		template<class T>
		inline idx_type CoTensor<T>::numel() const
		{
			return _rep->size() - _offset;
		}
		template<class T>
		inline idx_type CoTensor<T>::offset() const
		{
			return _offset;
		}
		template<class T>
		inline PlatformType CoTensor<T>::platform() const
		{
			return PlatformType::CPU;
		}
		template<class T>
		inline tensor::DimVector CoTensor<T>::size() const
		{
			return _dimensions;
		}
		template<class T>
		inline idx_type CoTensor<T>::size(idx_type i) const
		{
			auto shape_size = _dimensions.size();
			if (i >= 0 && i < _dimensions.size())
				return _dimensions[i];
			else if (i <= -1 && i >= -static_cast<idx_type>(_dimensions.size()))
				return _dimensions[shape_size + i];
			else
				throw std::runtime_error("Dimension out of range");
		}
		template<class T>
		inline tensor::Storage & CoTensor<T>::storage()
		{
			return *_rep;
		}
		template<class T>
		inline tensor::StrideVector CoTensor<T>::stride() const
		{
			return _strides;
		}
		template<class T>
		inline idx_type CoTensor<T>::stride(idx_type i) const
		{
			auto shape_size = _strides.size();
			if (i >= 0 && i < _strides.size())
				return _strides[i];
			else if (i <= -1 && i >= -static_cast<idx_type>(_strides.size()))
				return _strides[shape_size + i];
			else
				throw std::runtime_error("Dimension out of range");
		}
		template<class T>
		inline std::string CoTensor<T>::to_string() const
		{
			std::function<std::string(const CoTensor<T>& t, idx_type dim, idx_type idx)> to_string_impl =
				[&](const CoTensor<T>& t, idx_type dim, idx_type idx)->std::string {
				std::string result;
				if (dim == t.ndimension())
				{
					result += std::to_string(t.data_ptr()[idx]);
					return result;
				}

				for (idx_type i = 0; i < t.size(dim); ++i)
				{
					if (dim != t.ndimension() - 1 && i != 0) result += ",\n";
					if (dim != t.ndimension() - 1)	result += "[";
					result += to_string_impl(t, dim + 1, idx);
					if (i != t.size(dim) - 1 && dim == t.ndimension() - 1)
						result += ",";
					if (dim != t.ndimension() - 1) result += "]";

					idx += t.stride(dim);
				}

				return result;
			};

			std::string result;
			result += "[" + to_string_impl(*this, 0, 0) + "]";
			return result;
		}
	}
}

#endif // !COCONET_COTENSOR_TENSOR_H_
