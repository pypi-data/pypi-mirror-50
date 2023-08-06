#ifndef COCONET_COTENSOR_APPLY_H_
#define COCONET_COTENSOR_APPLY_H_

#include <vector>

#include <coconet/cotensor/tensor.h>

namespace coconet
{
	namespace cotensor
	{
		void add_scalar_(CoTensor<f32>& tensor, f32 value);
		void add_scalar_(CoTensor<f64>& tensor, f64 value);
		void add_scalar_(CoTensor<u8>& tensor, u8 value);
		void add_scalar_(CoTensor<i8>& tensor, i8 value);
		void add_scalar_(CoTensor<i16>& tensor, i16 value);
		void add_scalar_(CoTensor<i32>& tensor, i32 value);
		void add_scalar_(CoTensor<i64>& tensor, i64 value);

		void fill_(CoTensor<f32>& tensor, f32 value);
		void fill_(CoTensor<f64>& tensor, f64 value);
		void fill_(CoTensor<u8>& tensor, u8 value);
		void fill_(CoTensor<i8>& tensor, i8 value);
		void fill_(CoTensor<i16>& tensor, i16 value);
		void fill_(CoTensor<i32>& tensor, i32 value);
		void fill_(CoTensor<i64>& tensor, i64 value);
	}
}

#endif