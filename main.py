import model.db_migration_plan as migration
from datetime import datetime
import log

logger = log.get_logger('main_execution')

if __name__ == '__main__':
    # execution time
    start = datetime.now()
    logger.info(f'Migration plan started at {start}')

    # process creation of schemas for original model
    migration.execute_migration_plan('snow_flake')
    # execute insert into tables
    migration.populate_tables('snow_flake')

    # create star schema
    migration.execute_migration_plan('star_schema')
    # populate table from star schema model
    migration.populate_tables('star_schema')

    logger.info(f'Execution time takes {datetime.now() - start}')
