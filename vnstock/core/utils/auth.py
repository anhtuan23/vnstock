# vnstock/core/utils/auth.py

"""
User authentication and API key registration for vnstock.

Simple interface for users to register their API key.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def register_user(api_key: Optional[str] = None) -> bool:
    """
    User registration with optional API key parameter.
    
    Guides user through the registration process to set up their API key.
    If api_key is provided, uses it directly. Otherwise, shows interactive prompt.
    
    Args:
        api_key: Optional API key to register directly
        
    Returns:
        bool: True if registration successful, False otherwise
    """
    try:
        # Check vnai availability
        from vnstock.core import vnai
        vnai  # Use the import to avoid unused warning
    except ImportError:
        print("✗ Lỗi: vnai module không được tìm thấy")
        return False
    
    # If API key is provided as parameter, use it directly
    if api_key:
        return _register_api_key_directly(api_key)
    
    # Otherwise, show interactive registration
    return _register_interactive()


def _register_api_key_directly(api_key: str) -> bool:
    """
    Register API key directly without interactive prompts.
    
    Args:
        api_key: API key to register
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not api_key or len(api_key) < 10:
        print("✗ API key không hợp lệ")
        return False
    
    try:
        from vnstock.core import setup_api_key
        if setup_api_key(api_key):
            # Show masked API key after successful registration
            if len(api_key) > 8:
                masked_key = f"{api_key[:4]}***{api_key[-4:]}"
            else:
                masked_key = api_key[:8] + "***" if len(api_key) > 4 else "****"
            
            print(f"✓ API key đã được lưu thành công! {masked_key}")
            print("✓ Bạn đang sử dụng Phiên bản cộng đồng (60 requests/phút)")
            return True
    except Exception as e:
        logger.debug(f"Direct setup failed: {e}")
        print("✗ Không thể lưu API key")
    
    return False


def _register_interactive() -> bool:
    """
    Interactive registration with user prompts.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from vnstock.core import setup_api_key, check_api_key_status
    except ImportError:
        print("✗ Lỗi: vnai module không được tìm thấy")
        return False
    
    print("\n" + "="*70)
    print("  VNSTOCK - ĐĂNG KÝ API KEY")
    print("="*70)
    
    # Check if already registered
    try:
        status = check_api_key_status()
        if status.get('has_api_key'):
            # Show masked API key (first 4, last 4, with *** in middle)
            api_key = status.get('api_key_preview', '')
            if len(api_key) > 8:
                masked_key = f"{api_key[:4]}***{api_key[-4:]}"
            else:
                masked_key = api_key[:8] + "***" if len(api_key) > 4 else "****"
            
            print(f"\n✓ API key: {masked_key}")
            print(f"✓ Tier (Gói): {status.get('tier', 'unknown')}")
            print(f"✓ Giới hạn (Limits): {status.get('limits', {})}")
            
            change = input("\nBạn muốn thay đổi API key? [y/N]: ").strip().lower()
            if change != 'y':
                return True
    except Exception:
        pass
    
    print("""
🚀 Đăng ký API key để tăng giới hạn sử dụng:

  • Khách (Guest): 20 requests/phút - không cần đăng ký
  • Cộng đồng (Community): 60 requests/phút - đăng ký miễn phí
  • Tài trợ (Sponsor): 180-600 requests/phút

📌 Đăng nhập Google để tạo tài khoản và lấy API key miễn phí tại: https://vnstocks.com/login
""")
    
    # Get API key from user directly (no Enter step)
    max_attempts = 3
    for attempt in range(max_attempts):
        api_key = input("\nNhập API key của bạn: ").strip()
        
        if not api_key:
            print("✗ API key không được để trống")
            if attempt < max_attempts - 1:
                print(f"  Vui lòng thử lại ({max_attempts - attempt - 1} lần còn lại)")
            continue
        
        if len(api_key) < 10:
            print("✗ API key quá ngắn")
            if attempt < max_attempts - 1:
                print(f"  Vui lòng thử lại ({max_attempts - attempt - 1} lần còn lại)")
            continue
        
        # Try to save API key
        try:
            if setup_api_key(api_key):
                # Show masked API key after successful registration
                if len(api_key) > 8:
                    masked_key = f"{api_key[:4]}***{api_key[-4:]}"
                else:
                    masked_key = api_key[:8] + "***" if len(api_key) > 4 else "****"
                
                print(f"\n✓ API key đã được lưu thành công! {masked_key}")
                print("✓ Bạn đang sử dụng Phiên bản cộng đồng (60 requests/phút)")
                print("\n🎉 Đăng ký thành công!")
                return True
        except Exception as e:
            logger.debug(f"Setup failed: {e}")
            print("✗ Không thể lưu API key")
            if attempt < max_attempts - 1:
                print(f"  Vui lòng thử lại ({max_attempts - attempt - 1} lần còn lại)")
    
    print("\n✗ Đăng ký thất bại")
    return False


def change_api_key(api_key: str) -> bool:
    """
    Change API key directly.
    
    Args:
        api_key: New API key
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not api_key or len(api_key) < 10:
        print("✗ API key không hợp lệ")
        return False
    
    try:
        from vnstock.core import setup_api_key
        if setup_api_key(api_key):
            print("✓ API key đã được cập nhật")
            return True
    except Exception as e:
        logger.debug(f"Change failed: {e}")
        print("✗ Không thể cập nhật API key")
    
    return False


def check_status() -> Optional[dict]:
    """
    Check current registration status.
    
    Returns:
        dict: Status information or None if error
    """
    try:
        from vnstock.core import check_api_key_status
        status = check_api_key_status()
        
        if status.get('has_api_key'):
            print(f"✓ API key: {status.get('api_key_preview')}")
            print(f"  Tier: {status.get('tier')}")
            print(f"  Giới hạn: {status.get('limits', {}).get('per_minute')} requests/phút")
        else:
            print("✗ Chưa đăng ký API key")
            print("  Tier: Guest (20 requests/phút)")
        
        return status
    except Exception as e:
        logger.debug(f"Status check failed: {e}")
        print("✗ Không thể kiểm tra trạng thái")
        return None
