/*
 * Value key functions
 *
 * Copyright (C) 2009-2019, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _LIBREGF_VALUE_KEY_H )
#define _LIBREGF_VALUE_KEY_H

#include <common.h>
#include <types.h>

#include "libregf_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct libregf_value_key libregf_value_key_t;

struct libregf_value_key
{
	/* The name hash
	 */
	uint32_t name_hash;

	/* The name
	 */
	uint8_t *name;

	/* The name size
	 */
	uint16_t name_size;

	/* The value data type
	 */
	uint32_t data_type;

	/* The flags
	 */
	uint16_t flags;

	/* The value data offset
	 */
	uint32_t data_offset;

	/* The value data
	 */
	uint8_t *data;

	/* The value data offset
	 */
	uint32_t data_size;

	/* Value to indicate the value data is stored in the key
	 */
	uint8_t data_in_key;
};

int libregf_value_key_initialize(
     libregf_value_key_t **value_key,
     libcerror_error_t **error );

int libregf_value_key_free(
     libregf_value_key_t **value_key,
     libcerror_error_t **error );

int libregf_value_key_read_data(
     libregf_value_key_t *value_key,
     const uint8_t *data,
     size_t data_size,
     uint32_t value_key_hash,
     int ascii_codepage,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBREGF_VALUE_KEY_H ) */

