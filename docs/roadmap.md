
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

## Post-MVP Development

### Document Intelligence

- General-purpose document processing
- Support for inconsistent document templates
- PDF retrieval integration
- OCR and image understanding

### Retrieval and Model Optimization

- BM25 and advanced keyword retrieval
- Retrieval relevance thresholds
- Metadata filtering
- Reranking
- Quantitative retrieval evaluation
- LLM quality and latency benchmarking
- GPU memory optimization

### Application Improvements

- Improved UI and UX
- Streaming responses
- Persistent inference preferences
- Document revision management
- Ingestion rollback and error handling

### Production Readiness

- User authentication
- Role-based access control
- Audit logging
- Backup and recovery
- Data retention policies
- Offline operation verification
- Security and prompt injection testing
- Production deployment architecture
