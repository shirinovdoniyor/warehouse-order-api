# Ordered roadmap

One checkbox = one tested commit and push. Do not skip prerequisites.

- [ ] 01. Configuration and SQLAlchemy session setup; PostgreSQL URL from environment, isolated SQLite test database
- [ ] 02. User model and Alembic initial migration; unique normalized email, password hash, timestamps
- [ ] 03. Password hashing service with Argon2 and verification tests
- [ ] 04. Registration API with email validation, duplicate handling and password hashing
- [ ] 05. Login API with expiring JWT access tokens and generic invalid-credentials response
- [ ] 06. Current-user dependency and GET /users/me; reject invalid or expired tokens
- [ ] 07. Admin and member roles; registration cannot grant admin; authorization tests
- [ ] 08. Update own profile with validated fields; reject editing another user
- [ ] 09. Password change with current-password verification and tests
- [ ] 10. Product model and migration; SKU unique, decimal price, timestamps
- [ ] 11. Admin product create API; reject invalid prices and duplicate SKU
- [ ] 12. Product list and detail APIs with pagination and stable ordering
- [ ] 13. Admin product update API with field validation
- [ ] 14. Product search and filtering by SKU/name; pagination tests
- [ ] 15. Warehouse model, migration and admin create API
- [ ] 16. Warehouse list, detail and update APIs with permissions
- [ ] 17. Inventory model and migration with unique warehouse/product pair and nonnegative quantity
- [ ] 18. Stock receipt API and inventory movement audit records in one transaction
- [ ] 19. Inventory list with warehouse/product filters and pagination
- [ ] 20. Stock adjustment API with reason and nonnegative invariant
- [ ] 21. Order and order-item models and migration; immutable unit-price snapshots
- [ ] 22. Create draft order API with ownership and product validation
- [ ] 23. Order list/detail APIs; users can only access their own orders
- [ ] 24. Confirm order using PostgreSQL transaction and row locks; atomic stock decrement
- [ ] 25. Insufficient-stock rollback tests with a real PostgreSQL integration path
- [ ] 26. Idempotency key for order confirmation; duplicate requests cannot decrement stock twice
- [ ] 27. Cancel confirmed order with exactly-once stock restoration
- [ ] 28. Order state transition validation and audit trail
- [ ] 29. Admin order filtering by status/date and pagination
- [ ] 30. Low-stock reporting endpoint with role restrictions
- [ ] 31. Sales summary endpoint using decimal totals and documented date boundaries
- [ ] 32. CSV export of authorized inventory records; formula injection protection
- [ ] 33. Consistent pagination response schemas across list APIs
- [ ] 34. Consistent error responses without internal exception details
- [ ] 35. API examples and architecture explanation based only on implemented features
