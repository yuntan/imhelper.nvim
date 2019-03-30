import ctypes
import pynvim

user32 = ctypes.windll.user32
imm32 = ctypes.windll.imm32

def get_hWnd():
    return imm32.ImmGetDefaultIMEWnd(user32.GetForegroundWindow())

def activate_im(hWnd):
    return user32.SendMessageW(hWnd, 0x283, 0x006, 0x001)

def deactivate_im(hWnd):
    return user32.SendMessageW(hWnd, 0x283, 0x006, 0x000)

def im_is_on(hWnd):
    return user32.SendMessageW(hWnd, 0x283, 0x005, 0x000)

@pynvim.plugin
class ImHelper(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.should_activate_im = False

    @pynvim.autocmd('InsertEnter')
    def on_insertenter(self):
        if not self.should_activate_im:
            return
        activate_im(get_hWnd())

    @pynvim.autocmd('InsertLeave')
    def on_insertleave(self):
        hWnd = get_hWnd()
        self.should_activate_im = im_is_on(hWnd)
        deactivate_im(hWnd)
