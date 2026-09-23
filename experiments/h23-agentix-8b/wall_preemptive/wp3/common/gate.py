"""挂起门: 抢占者写, 受害者读。1 字节 mmap: b'0'=运行, b'1'=挂起。"""
import mmap, os
class SuspendGate:
    def __init__(self, path, create=False):
        if create or not os.path.exists(path):
            with open(path,'wb') as f: f.write(b'0')
        self.f=open(path,'r+b'); self.m=mmap.mmap(self.f.fileno(),1)
    def set(self, suspended: bool): self.m[0] = 0x31 if suspended else 0x30
    def suspended(self) -> bool: return self.m[0]==0x31
    def close(self):
        try: self.m.close(); self.f.close()
        except Exception: pass
