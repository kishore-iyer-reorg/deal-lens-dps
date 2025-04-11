from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "financial_data" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "boolean_value" BOOL,
    "term_sheet_status" VARCHAR(30),
    "numeric_value" DOUBLE PRECISION,
    "date_value" DATE,
    "composite_value_type" VARCHAR(20),
    "composite_value_data" JSONB,
    "percentage_multiple_type" VARCHAR(30),
    "percentage_multiple_data" JSONB,
    "names_list_type" VARCHAR(15),
    "names_list_data" JSONB,
    "financial_ratio_type" VARCHAR(30),
    "financial_ratio_data" JSONB,
    "percentage_condition_type" VARCHAR(30),
    "percentage_condition_data" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "financial_data"."term_sheet_status" IS 'YES: Yes\nPARTIAL: Partial\nNO: No\nNA: N/A\nNOT_STATED: Not stated in Term Sheet';
COMMENT ON COLUMN "financial_data"."composite_value_type" IS 'NUMBER: number\nGREATER_OF: greater_of\nNO_MINIMUM: no_minimum\nNO_PIK: no_pik';
COMMENT ON COLUMN "financial_data"."percentage_multiple_type" IS 'PERCENTAGE: percentage\nNO_CASH_REQUIREMENT: no_cash_requirement\nNOT_STATED: not_stated';
COMMENT ON COLUMN "financial_data"."names_list_type" IS 'NAMES_LIST: names_list\nNA: na';
COMMENT ON COLUMN "financial_data"."financial_ratio_type" IS 'FIRST_LIEN: first_lien\nSENIOR_SECURED: senior_secured\nSECURED: secured\nTOTAL_NET: total_net\nFIXED_CHARGE: fixed_charge\nINTEREST_COVERAGE: interest_coverage\nNO_COVENANT: no_covenant\nNOT_STATED: not_stated';
COMMENT ON COLUMN "financial_data"."percentage_condition_type" IS 'WITH_LEVERAGE_TEST: with_leverage_test\nNO_LEVERAGE_TEST: no_leverage_test\nBASKET_NO_COMPONENT: basket_no_component\nNO_BASKET: no_basket\nNOT_STATED: not_stated';
COMMENT ON TABLE "financial_data" IS 'Tortoise ORM model for financial data storage';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
