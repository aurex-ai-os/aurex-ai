from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)
driver.get("http://localhost:8080")
import time
time.sleep(2)

# set theme to synapse
driver.execute_script("window.applyBgPattern('synapse');")
time.sleep(1)

# Check canvas
result = driver.execute_script("""
const c = document.getElementById('synapse-canvas');
if (!c) return 'No canvas found';
const rect = c.getBoundingClientRect();
const style = window.getComputedStyle(c);
return {
  rect: rect,
  opacity: style.opacity,
  zIndex: style.zIndex,
  display: style.display,
  pointerEvents: style.pointerEvents,
  bodyBg: window.getComputedStyle(document.body).backgroundColor,
  bodyBgImg: window.getComputedStyle(document.body).backgroundImage
};
""")
print(result)
driver.quit()
