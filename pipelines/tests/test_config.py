from domainmind.training.config import QLoRAConfig


def test_qlora_defaults():
    cfg = QLoRAConfig()
    assert cfg.lora_r == 16
    assert cfg.lora_alpha == 32
    assert cfg.lora_alpha / cfg.lora_r == 2.0
    assert cfg.load_in_4bit is True
