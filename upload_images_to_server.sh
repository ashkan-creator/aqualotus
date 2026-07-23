#!/bin/bash
echo "در حال انتقال عکس‌های محلی به سرور..."
if [ -d "./backend/uploads" ]; then
    echo "پوشه backend/uploads یافت شد."
elif [ -d "./uploads" ]; then
    echo "پوشه uploads یافت شد."
else
    echo "هیچ پوشه آپلودی پیدا نشد!"
fi
