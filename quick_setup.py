#!/usr/bin/env python3
"""
Quick setup script for TenGuard Watch automation
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "requests", "beautifulsoup4", "lxml"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_automation():
    """Test the automation script"""
    print("🧪 Testing automation...")
    try:
        result = subprocess.run([sys.executable, "auto_news_updater.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Automation test successful!")
            return True
        else:
            print(f"❌ Automation test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Automation test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing automation: {e}")
        return False

def setup_cron():
    """Set up cron job for automation"""
    print("⏰ Setting up automated scheduling...")
    current_dir = os.getcwd()
    cron_command = f"0 9 * * 1 cd {current_dir} && {sys.executable} auto_news_updater.py"
    
    try:
        # Get current crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""
        
        # Check if our job already exists
        if "auto_news_updater.py" not in current_crontab:
            # Add our job
            new_crontab = current_crontab + f"\n{cron_command}\n" if current_crontab else f"{cron_command}\n"
            subprocess.run(["crontab", "-"], input=new_crontab, text=True)
            print("✅ Cron job added successfully!")
            print(f"   Schedule: Every Monday at 9 AM")
            print(f"   Command: {cron_command}")
        else:
            print("✅ Cron job already exists!")
        return True
    except Exception as e:
        print(f"❌ Error setting up cron: {e}")
        print("   You can set it up manually with:")
        print(f"   crontab -e")
        print(f"   Then add: {cron_command}")
        return False

def main():
    """Main setup function"""
    print("🚀 TenGuard Watch Automation Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("tenguardwatch.html"):
        print("❌ tenguardwatch.html not found in current directory!")
        print("   Please run this script from your website directory.")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Test automation
    if not test_automation():
        print("⚠️  Automation test failed, but you can still set up scheduling.")
    
    # Set up cron
    setup_cron()
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Your website will update automatically every Monday at 9 AM")
    print("2. Run 'python3 auto_news_updater.py' to update manually")
    print("3. Run 'python3 check_status.py' to check update status")
    print("4. Check 'news_updater.log' for detailed logs")
    
    print("\n🔧 Manual Commands:")
    print("   Update now: python3 auto_news_updater.py")
    print("   Check status: python3 check_status.py")
    print("   View logs: tail -f news_updater.log")

if __name__ == "__main__":
    main()
