─────────────────────────────
1. Presentation Layer
─────────────────────────────
-  Role: Handles user interaction and displays output.
-  Components: Controllers, views (UI components), request/response handlers.
-  Responsibilities:
    *   Capture and validate user input.
    *   Delegate requests to the business layer.
    *   Render responses and feedback.

─────────────────────────────
2. Business/Domain Logic Layer
─────────────────────────────
-  Role: Encapsulates core business rules and domain concepts.
-  Components: Domain models, service classes, and business rules.
-  Responsibilities:
    *   Process business logic and validation.
    *   Coordinate activities between layers.
    *   Enforce domain invariants.

─────────────────────────────
3. Data Access Layer (Persistence)
─────────────────────────────
-  Role: Manages interactions with data sources.
-  Components: Repositories, data mappers, DAO classes.
-  Responsibilities:
    *   Abstract database or external storage operations.
    *   Provide CRUD functions.
    *   Map domain objects to persistent structures.

─────────────────────────────
4. Infrastructure/Integration Layer
─────────────────────────────
-  Role: Supports cross-cutting concerns and external integrations.
-  Components: Logging, caching, messaging, API clients, configuration.
-  Responsibilities:
    *   Facilitate communication with third-party services.
    *   Handle technical concerns (security, error handling).
    *   Manage environment-specific configurations.

─────────────────────────────
Overall Application Workflow
─────────────────────────────
1. The Presentation Layer accepts requests from users and passes them to the Business Layer after preliminary validation.
2. The Business Layer processes these requests per established business rules, interfacing with the Data Access Layer when persistent operations are needed.
3. The Data Access Layer retrieves or updates data, while the Infrastructure Layer supports auxiliary operations (like logging or external API calls).
4. Responses are aggregated and sent back up the chain for user presentation.


![Diagram](https://www.plantuml.com/plantuml/png/lLX1Szis4xthL-puErYUJqvwwi7ZUEB4yTGpISSJnxro860b8G415hkKexRvxoL0KX14CSeXha_ouhst2s2v2-0riV1SbsP2KXY4NrxyEc7D1k6wgeoMWhMpSEtbIZDAhZt2MoE8aE16YwKNvMHo2gz-vb-ZT--Hq7Bh_BtOeF_fJYeXluWbmidGrmdyFG4uXGVqQ_GWs_bEeFq5RsjYLrxJnieE4U00_uzBEJs32rWxhLfRiH9M6IoaqMXvwb4ez3DuyfhHxq2_JRRw7rtDILGeLVXWcLQ2LpDezNpknICviyP6_iyQYSFWHwJAMS9U-nJUnX1Q9saoAy7TGETGEcjHxiz3QJeyG6XLqVcTbiWhfsRGXge4Yq4e036Ow_ix47DYBsHOU4gpRwNI_udS6jvPLJbjUVBjEJBlJKtQ8j7B6rSAtII4Mshvt2auuZJbOjgha75QudQpF0h6eYRqq-5o1yGIEGuNMWqGcOPir8U8B2N6FH0Bhca8o1BxLXlSYx-kZ1Fg2E_EhZNlCvTeqOUuTHmjZBPVHW8KKcB57N3AxWlQ6NHhCkxr0nA9PUwsI_Uo7JeSzhEavOrW0TTI8b6R5p2zHq-Q6At4i-TBpSnnIiZ-q-tMweqW_8YL8ytERzBc4dgUklddi4YVjjaorIet5CAOQKWXBD7o39nNw8lvvfMjZPc1qQNc-3lG7aA1i18lFrrrfGaDCaRHl9oUmZOcZNd9ou9DNq7QqW0AEXah9F0eKpQ0GgiPB1fKbrazQQ3KflJHA18qhTLyKyGKRXDvW4hhhgCfBSfU25r-7vzFb-tzb18rnTI8Sj7Xg6TcczLHhXAdjg4P3bWpY6A4QCS4qZo-ko6ANL0OhF_HYJlBQ3bmMsXEVoJqeznGLQmeCP03CDksVZ17FTxT3FHJYexuY0kLrdbBIcU64iivUkhHbE1zGkJj8Opsw7phWkxulXNIrPOF1gKj7t1oBFvy9OviLXBBipHHirD7rry_E8M60AqK5TL6C2fepBn2kBb-to2tvQz5jZLlDwpE073Ux-K54FlUgAaGalMwiSwTCz4SWjZz_fB48NhbzLfmuaUxUx9njctM9DKyiPDmbycjTaAdRoT1Gz7AuiZuymqZ3HIof1iKbjpQby5X4Kmnn88sNCVGl56DhEJ8Hj_P5NhDmae4ZoOUxccbAuAft-a9e1hK6c7XNRdNnCuci6U1ot_Ep_UwnpWeJlWeC2t3SMXQsgFO7_BzesAfu1q1_SZI7Fwed-VGT6SNNX3xkhstlcmCZ4l_dzmgZ_bEjyntNoLM-HqehDixxvtlBP7jhJ2vzO6zQ5GtkVNHKbrLpZEg-msldFq3FJNwEIgao6CyVUVstntVkjfsrX1Xk8uijLs2i0eUaBdvJI1TMJcBbbFO0HTBOpeNHCjqMrX2QMvHwMEDtAJRii-hJR56Vm7P37fG2r7pYtWkdWl2V8JG1t9tWKzZgRSCT3FdfRP5AJuxt_QmPDCssP9M7aIIgRtfgba2Pp4bwChHJfa-3xktutjUBnRe2z9_OH5BySwOmdczJCMn2LHyBK8rFmplssGyKn-mhpI53t9qN3P-b7ko1Q5qLdNIgNn7hrbu2r4RBcAlh-lKkmQ3MVT9Ox719-9mS9_8kaHNyrw0gJNyXgP23ulQjYyFy19K0_M2dS-V8RH7olBafiV1vILC7sV_kxszRlxEuEggpthVyOeg4ejrovp6exCmHiptJgFXCv6rzsYv2A4JYx8Qrpy8Z-fAC0RBCrv2iKAhq4gD17Fa9qGB9jGoWgaIj485mdltHA2jqb8mWkevcxFdVYTiNH4uktt50HDUKYRTYzgB5rVP6ye5d4XX39rCqYjO1FLlKBavNVDttedQ-KDDIDabtU_UF7UT1g6yKOOu0lzaW4kTzpXkJBFhjRlmpdGKdOBz3YEUNWQ4Q3s8lzKcGuV_nt6vwXXssEirWVIEw5pMiT1UJ0Qlja4rjPsG2yukzBBsGV4mkcrT0MjSmrbhaU_562O_1ut2NgDLTMd-1G00)
