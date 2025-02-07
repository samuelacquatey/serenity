from vertexai.preview.tuning import sft

base_model = 'gemini-1.5-flash-002'  # Fast & efficient
tuned_model_display_name = "ai-therapist-v01"

sft_tuning_job = sft.train(
    source_model=base_model,
    train_dataset="gs://your-bucket/therapy_train.jsonl",
    validation_dataset="gs://your-bucket/therapy_validation.jsonl",
    tuned_model_display_name=tuned_model_display_name
)
