
# Document Preprocessing Improvements

Status: Deferred

## Current Limitations

- Maintenance records use inconsistent Excel layouts.
- Fixed cell mapping supports only known templates.
- Unsupported templates may fail during normalization.
- PDF normalization is not yet implemented.

## Future Improvements

- Dynamic field extraction based on semantic labels
- Automatic document template detection
- Support for inconsistent Excel layouts
- Rule-based and LLM-based hybrid extraction
- PDF table and layout recognition
- OCR for scanned documents
- Extraction accuracy validation
- Standardized maintenance record schema
- Manual review of uncertain extracted values

## Development Decision

Prioritize core RAG application features before
improving document preprocessing.

Avoid adding individual mapping rules for every
maintenance document template.
