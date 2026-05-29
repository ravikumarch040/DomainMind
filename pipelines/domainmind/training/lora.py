"""Attach LoRA and build SFTTrainer — LLD §3.3."""

from datasets import Dataset
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments
from trl import DataCollatorForCompletionOnlyLM, SFTTrainer

from domainmind.training.config import QLoRAConfig
from domainmind.training.model import assert_training_ready


def attach_lora(model, cfg: QLoRAConfig):
    lora_config = LoraConfig(
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        target_modules=cfg.lora_target_modules,
        lora_dropout=cfg.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def build_trainer(
    model,
    tokenizer,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    cfg: QLoRAConfig,
) -> SFTTrainer:
    training_args = TrainingArguments(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        lr_scheduler_type=cfg.lr_scheduler_type,
        warmup_ratio=cfg.warmup_ratio,
        weight_decay=cfg.weight_decay,
        max_grad_norm=cfg.max_grad_norm,
        optim=cfg.optim,
        fp16=cfg.fp16,
        bf16=cfg.bf16,
        gradient_checkpointing=cfg.gradient_checkpointing,
        logging_steps=cfg.logging_steps,
        save_strategy=cfg.save_strategy,
        save_steps=cfg.save_steps,
        eval_steps=cfg.eval_steps,
        eval_strategy="steps",
        load_best_model_at_end=cfg.load_best_model_at_end,
        report_to=cfg.report_to,
    )

    collator = DataCollatorForCompletionOnlyLM(cfg.response_template, tokenizer=tokenizer)
    assert_training_ready(model, collator)

    return SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        dataset_text_field="text",
        max_seq_length=cfg.max_seq_length,
        data_collator=collator,
        packing=cfg.packing,
        args=training_args,
    )
