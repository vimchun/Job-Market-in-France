# HELP go_gc_duration_seconds A summary of the wall-time pause (stop-the-world) duration in garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 3.7844e-05
go_gc_duration_seconds{quantile="0.25"} 0.00014305
go_gc_duration_seconds{quantile="0.5"} 0.000231817
go_gc_duration_seconds{quantile="0.75"} 0.000403849
go_gc_duration_seconds{quantile="1"} 0.059968797
go_gc_duration_seconds_sum 3.780293349
go_gc_duration_seconds_count 2948


# HELP go_gc_gogc_percent Heap size target percentage configured by the user, otherwise 100. This value is set by the GOGC environment variable, and the runtime/debug.SetGCPercent function. Sourced from /gc/gogc:percent
# TYPE go_gc_gogc_percent gauge
go_gc_gogc_percent 100


# HELP go_gc_gomemlimit_bytes Go runtime memory limit configured by the user, otherwise math.MaxInt64. This value is set by the GOMEMLIMIT environment variable, and the runtime/debug.SetMemoryLimit function. Sourced from /gc/gomemlimit:bytes
# TYPE go_gc_gomemlimit_bytes gauge
go_gc_gomemlimit_bytes 9.223372036854776e+18


# HELP go_goroutines Number of goroutines that currently exist.
# TYPE go_goroutines gauge
go_goroutines 16


# HELP go_info Information about the Go environment.
# TYPE go_info gauge
go_info{version="go1.23.6"} 1


# HELP go_memstats_alloc_bytes Number of bytes allocated in heap and currently in use. Equals to /memory/classes/heap/objects:bytes.
# TYPE go_memstats_alloc_bytes gauge
go_memstats_alloc_bytes 2.945248e+06


# HELP go_memstats_alloc_bytes_total Total number of bytes allocated in heap until now, even if released already. Equals to /gc/heap/allocs:bytes.
# TYPE go_memstats_alloc_bytes_total counter
go_memstats_alloc_bytes_total 4.80011448e+09


# HELP go_memstats_buck_hash_sys_bytes Number of bytes used by the profiling bucket hash table. Equals to /memory/classes/profiling/buckets:bytes.
# TYPE go_memstats_buck_hash_sys_bytes gauge
go_memstats_buck_hash_sys_bytes 4257


# HELP go_memstats_frees_total Total number of heap objects frees. Equals to /gc/heap/frees:objects + /gc/heap/tiny/allocs:objects.
# TYPE go_memstats_frees_total counter
go_memstats_frees_total 8.4352836e+07


# HELP go_memstats_gc_sys_bytes Number of bytes used for garbage collection system metadata. Equals to /memory/classes/metadata/other:bytes.
# TYPE go_memstats_gc_sys_bytes gauge
go_memstats_gc_sys_bytes 2.906384e+06


# HELP go_memstats_heap_alloc_bytes Number of heap bytes allocated and currently in use, same as go_memstats_alloc_bytes. Equals to /memory/classes/heap/objects:bytes.
# TYPE go_memstats_heap_alloc_bytes gauge
go_memstats_heap_alloc_bytes 2.945248e+06


# HELP go_memstats_heap_idle_bytes Number of heap bytes waiting to be used. Equals to /memory/classes/heap/released:bytes + /memory/classes/heap/free:bytes.
# TYPE go_memstats_heap_idle_bytes gauge
go_memstats_heap_idle_bytes 1.1157504e+07


# HELP go_memstats_heap_inuse_bytes Number of heap bytes that are in use. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes
# TYPE go_memstats_heap_inuse_bytes gauge
go_memstats_heap_inuse_bytes 4.849664e+06


# HELP go_memstats_heap_objects Number of currently allocated objects. Equals to /gc/heap/objects:objects.
# TYPE go_memstats_heap_objects gauge
go_memstats_heap_objects 39057


# HELP go_memstats_heap_released_bytes Number of heap bytes released to OS. Equals to /memory/classes/heap/released:bytes.
# TYPE go_memstats_heap_released_bytes gauge
go_memstats_heap_released_bytes 9.486336e+06


# HELP go_memstats_heap_sys_bytes Number of heap bytes obtained from system. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes + /memory/classes/heap/released:bytes + /memory/classes/heap/free:bytes.
# TYPE go_memstats_heap_sys_bytes gauge
go_memstats_heap_sys_bytes 1.6007168e+07


# HELP go_memstats_last_gc_time_seconds Number of seconds since 1970 of last garbage collection.
# TYPE go_memstats_last_gc_time_seconds gauge
go_memstats_last_gc_time_seconds 1.7519351490165837e+09


# HELP go_memstats_mallocs_total Total number of heap objects allocated, both live and gc-ed. Semantically a counter version for go_memstats_heap_objects gauge. Equals to /gc/heap/allocs:objects + /gc/heap/tiny/allocs:objects.
# TYPE go_memstats_mallocs_total counter
go_memstats_mallocs_total 8.4391893e+07


# HELP go_memstats_mcache_inuse_bytes Number of bytes in use by mcache structures. Equals to /memory/classes/metadata/mcache/inuse:bytes.
# TYPE go_memstats_mcache_inuse_bytes gauge
go_memstats_mcache_inuse_bytes 4800


# HELP go_memstats_mcache_sys_bytes Number of bytes used for mcache structures obtained from system. Equals to /memory/classes/metadata/mcache/inuse:bytes + /memory/classes/metadata/mcache/free:bytes.
# TYPE go_memstats_mcache_sys_bytes gauge
go_memstats_mcache_sys_bytes 15600


# HELP go_memstats_mspan_inuse_bytes Number of bytes in use by mspan structures. Equals to /memory/classes/metadata/mspan/inuse:bytes.
# TYPE go_memstats_mspan_inuse_bytes gauge
go_memstats_mspan_inuse_bytes 116320


# HELP go_memstats_mspan_sys_bytes Number of bytes used for mspan structures obtained from system. Equals to /memory/classes/metadata/mspan/inuse:bytes + /memory/classes/metadata/mspan/free:bytes.
# TYPE go_memstats_mspan_sys_bytes gauge
go_memstats_mspan_sys_bytes 179520


# HELP go_memstats_next_gc_bytes Number of heap bytes when next garbage collection will take place. Equals to /gc/heap/goal:bytes.
# TYPE go_memstats_next_gc_bytes gauge
go_memstats_next_gc_bytes 6.044648e+06


# HELP go_memstats_other_sys_bytes Number of bytes used for other system allocations. Equals to /memory/classes/other:bytes.
# TYPE go_memstats_other_sys_bytes gauge
go_memstats_other_sys_bytes 800815


# HELP go_memstats_stack_inuse_bytes Number of bytes obtained from system for stack allocator in non-CGO environments. Equals to /memory/classes/heap/stacks:bytes.
# TYPE go_memstats_stack_inuse_bytes gauge
go_memstats_stack_inuse_bytes 753664


# HELP go_memstats_stack_sys_bytes Number of bytes obtained from system for stack allocator. Equals to /memory/classes/heap/stacks:bytes + /memory/classes/os-stacks:bytes.
# TYPE go_memstats_stack_sys_bytes gauge
go_memstats_stack_sys_bytes 753664


# HELP go_memstats_sys_bytes Number of bytes obtained from system. Equals to /memory/classes/total:byte.
# TYPE go_memstats_sys_bytes gauge
go_memstats_sys_bytes 2.0667408e+07


# HELP go_sched_gomaxprocs_threads The current runtime.GOMAXPROCS setting, or the number of operating system threads that can execute user-level Go code simultaneously. Sourced from /sched/gomaxprocs:threads
# TYPE go_sched_gomaxprocs_threads gauge
go_sched_gomaxprocs_threads 4


# HELP go_threads Number of OS threads created.
# TYPE go_threads gauge
go_threads 9


# HELP pg_database_connection_limit Connection limit set for the database
# TYPE pg_database_connection_limit gauge
pg_database_connection_limit{datname="francetravail"} -1
pg_database_connection_limit{datname="postgres"} -1
pg_database_connection_limit{datname="template0"} -1
pg_database_connection_limit{datname="template1"} -1


# HELP pg_database_size_bytes Disk space used by the database
# TYPE pg_database_size_bytes gauge
pg_database_size_bytes{datname="francetravail"} 2.56782819e+08
pg_database_size_bytes{datname="postgres"} 7.696867e+06
pg_database_size_bytes{datname="template0"} 7.537167e+06
pg_database_size_bytes{datname="template1"} 7.754211e+06


# HELP pg_exporter_last_scrape_duration_seconds Duration of the last scrape of metrics from PostgreSQL.
# TYPE pg_exporter_last_scrape_duration_seconds gauge
pg_exporter_last_scrape_duration_seconds 0.096679118


# HELP pg_exporter_last_scrape_error Whether the last scrape of metrics from PostgreSQL resulted in an error (1 for error, 0 for success).
# TYPE pg_exporter_last_scrape_error gauge
pg_exporter_last_scrape_error 0


# HELP pg_exporter_scrapes_total Total number of times PostgreSQL was scraped for metrics.
# TYPE pg_exporter_scrapes_total counter
pg_exporter_scrapes_total 1447


# HELP pg_locks_count Number of locks
# TYPE pg_locks_count gauge
pg_locks_count{datname="francetravail",mode="accessexclusivelock"} 0
pg_locks_count{datname="francetravail",mode="accesssharelock"} 1
pg_locks_count{datname="francetravail",mode="exclusivelock"} 0
pg_locks_count{datname="francetravail",mode="rowexclusivelock"} 0
pg_locks_count{datname="francetravail",mode="rowsharelock"} 0
pg_locks_count{datname="francetravail",mode="sharelock"} 0
pg_locks_count{datname="francetravail",mode="sharerowexclusivelock"} 0
pg_locks_count{datname="francetravail",mode="shareupdateexclusivelock"} 0
pg_locks_count{datname="francetravail",mode="sireadlock"} 0
pg_locks_count{datname="postgres",mode="accessexclusivelock"} 0
pg_locks_count{datname="postgres",mode="accesssharelock"} 0
pg_locks_count{datname="postgres",mode="exclusivelock"} 0
pg_locks_count{datname="postgres",mode="rowexclusivelock"} 0
pg_locks_count{datname="postgres",mode="rowsharelock"} 0
pg_locks_count{datname="postgres",mode="sharelock"} 0
pg_locks_count{datname="postgres",mode="sharerowexclusivelock"} 0
pg_locks_count{datname="postgres",mode="shareupdateexclusivelock"} 0
pg_locks_count{datname="postgres",mode="sireadlock"} 0
pg_locks_count{datname="template0",mode="accessexclusivelock"} 0
pg_locks_count{datname="template0",mode="accesssharelock"} 0
pg_locks_count{datname="template0",mode="exclusivelock"} 0
pg_locks_count{datname="template0",mode="rowexclusivelock"} 0
pg_locks_count{datname="template0",mode="rowsharelock"} 0
pg_locks_count{datname="template0",mode="sharelock"} 0
pg_locks_count{datname="template0",mode="sharerowexclusivelock"} 0
pg_locks_count{datname="template0",mode="shareupdateexclusivelock"} 0
pg_locks_count{datname="template0",mode="sireadlock"} 0
pg_locks_count{datname="template1",mode="accessexclusivelock"} 0
pg_locks_count{datname="template1",mode="accesssharelock"} 0
pg_locks_count{datname="template1",mode="exclusivelock"} 0
pg_locks_count{datname="template1",mode="rowexclusivelock"} 0
pg_locks_count{datname="template1",mode="rowsharelock"} 0
pg_locks_count{datname="template1",mode="sharelock"} 0
pg_locks_count{datname="template1",mode="sharerowexclusivelock"} 0
pg_locks_count{datname="template1",mode="shareupdateexclusivelock"} 0
pg_locks_count{datname="template1",mode="sireadlock"} 0


# HELP pg_replication_is_replica Indicates if the server is a replica
# TYPE pg_replication_is_replica gauge
pg_replication_is_replica 0


# HELP pg_replication_lag_seconds Replication lag behind master in seconds
# TYPE pg_replication_lag_seconds gauge
pg_replication_lag_seconds 0


# HELP pg_replication_last_replay_seconds Age of last replay in seconds
# TYPE pg_replication_last_replay_seconds gauge
pg_replication_last_replay_seconds 0


# HELP pg_roles_connection_limit Connection limit set for the role
# TYPE pg_roles_connection_limit gauge
pg_roles_connection_limit{rolname="mhh"} -1
pg_roles_connection_limit{rolname="pg_checkpoint"} -1
pg_roles_connection_limit{rolname="pg_create_subscription"} -1
pg_roles_connection_limit{rolname="pg_database_owner"} -1
pg_roles_connection_limit{rolname="pg_execute_server_program"} -1
pg_roles_connection_limit{rolname="pg_monitor"} -1
pg_roles_connection_limit{rolname="pg_read_all_data"} -1
pg_roles_connection_limit{rolname="pg_read_all_settings"} -1
pg_roles_connection_limit{rolname="pg_read_all_stats"} -1
pg_roles_connection_limit{rolname="pg_read_server_files"} -1
pg_roles_connection_limit{rolname="pg_signal_backend"} -1
pg_roles_connection_limit{rolname="pg_stat_scan_tables"} -1
pg_roles_connection_limit{rolname="pg_use_reserved_connections"} -1
pg_roles_connection_limit{rolname="pg_write_all_data"} -1
pg_roles_connection_limit{rolname="pg_write_server_files"} -1


# HELP pg_scrape_collector_duration_seconds postgres_exporter: Duration of a collector scrape.
# TYPE pg_scrape_collector_duration_seconds gauge
pg_scrape_collector_duration_seconds{collector="database"} 0.132171559
pg_scrape_collector_duration_seconds{collector="locks"} 0.037191249
pg_scrape_collector_duration_seconds{collector="replication"} 0.114529104
pg_scrape_collector_duration_seconds{collector="replication_slot"} 0.119337555
pg_scrape_collector_duration_seconds{collector="roles"} 0.116983123
pg_scrape_collector_duration_seconds{collector="stat_bgwriter"} 0.123511856
pg_scrape_collector_duration_seconds{collector="stat_database"} 0.122258128
pg_scrape_collector_duration_seconds{collector="stat_user_tables"} 0.111005179
pg_scrape_collector_duration_seconds{collector="statio_user_tables"} 0.030714787
pg_scrape_collector_duration_seconds{collector="wal"} 0.038958458


# HELP pg_scrape_collector_success postgres_exporter: Whether a collector succeeded.
# TYPE pg_scrape_collector_success gauge
pg_scrape_collector_success{collector="database"} 1
pg_scrape_collector_success{collector="locks"} 1
pg_scrape_collector_success{collector="replication"} 1
pg_scrape_collector_success{collector="replication_slot"} 1
pg_scrape_collector_success{collector="roles"} 1
pg_scrape_collector_success{collector="stat_bgwriter"} 1
pg_scrape_collector_success{collector="stat_database"} 1
pg_scrape_collector_success{collector="stat_user_tables"} 1
pg_scrape_collector_success{collector="statio_user_tables"} 1
pg_scrape_collector_success{collector="wal"} 1


# HELP pg_settings_allow_in_place_tablespaces Server Parameter: allow_in_place_tablespaces
# TYPE pg_settings_allow_in_place_tablespaces gauge
pg_settings_allow_in_place_tablespaces{server="postgres:5432"} 0


# HELP pg_settings_allow_system_table_mods Server Parameter: allow_system_table_mods
# TYPE pg_settings_allow_system_table_mods gauge
pg_settings_allow_system_table_mods{server="postgres:5432"} 0


# HELP pg_settings_archive_timeout_seconds Server Parameter: archive_timeout [Units converted to seconds.]
# TYPE pg_settings_archive_timeout_seconds gauge
pg_settings_archive_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_array_nulls Server Parameter: array_nulls
# TYPE pg_settings_array_nulls gauge
pg_settings_array_nulls{server="postgres:5432"} 1


# HELP pg_settings_authentication_timeout_seconds Server Parameter: authentication_timeout [Units converted to seconds.]
# TYPE pg_settings_authentication_timeout_seconds gauge
pg_settings_authentication_timeout_seconds{server="postgres:5432"} 60


# HELP pg_settings_autovacuum Server Parameter: autovacuum
# TYPE pg_settings_autovacuum gauge
pg_settings_autovacuum{server="postgres:5432"} 1


# HELP pg_settings_autovacuum_analyze_scale_factor Server Parameter: autovacuum_analyze_scale_factor
# TYPE pg_settings_autovacuum_analyze_scale_factor gauge
pg_settings_autovacuum_analyze_scale_factor{server="postgres:5432"} 0.1


# HELP pg_settings_autovacuum_analyze_threshold Server Parameter: autovacuum_analyze_threshold
# TYPE pg_settings_autovacuum_analyze_threshold gauge
pg_settings_autovacuum_analyze_threshold{server="postgres:5432"} 50


# HELP pg_settings_autovacuum_freeze_max_age Server Parameter: autovacuum_freeze_max_age
# TYPE pg_settings_autovacuum_freeze_max_age gauge
pg_settings_autovacuum_freeze_max_age{server="postgres:5432"} 2e+08


# HELP pg_settings_autovacuum_max_workers Server Parameter: autovacuum_max_workers
# TYPE pg_settings_autovacuum_max_workers gauge
pg_settings_autovacuum_max_workers{server="postgres:5432"} 3


# HELP pg_settings_autovacuum_multixact_freeze_max_age Server Parameter: autovacuum_multixact_freeze_max_age
# TYPE pg_settings_autovacuum_multixact_freeze_max_age gauge
pg_settings_autovacuum_multixact_freeze_max_age{server="postgres:5432"} 4e+08


# HELP pg_settings_autovacuum_naptime_seconds Server Parameter: autovacuum_naptime [Units converted to seconds.]
# TYPE pg_settings_autovacuum_naptime_seconds gauge
pg_settings_autovacuum_naptime_seconds{server="postgres:5432"} 60


# HELP pg_settings_autovacuum_vacuum_cost_delay_seconds Server Parameter: autovacuum_vacuum_cost_delay [Units converted to seconds.]
# TYPE pg_settings_autovacuum_vacuum_cost_delay_seconds gauge
pg_settings_autovacuum_vacuum_cost_delay_seconds{server="postgres:5432"} 0.002


# HELP pg_settings_autovacuum_vacuum_cost_limit Server Parameter: autovacuum_vacuum_cost_limit
# TYPE pg_settings_autovacuum_vacuum_cost_limit gauge
pg_settings_autovacuum_vacuum_cost_limit{server="postgres:5432"} -1


# HELP pg_settings_autovacuum_vacuum_insert_scale_factor Server Parameter: autovacuum_vacuum_insert_scale_factor
# TYPE pg_settings_autovacuum_vacuum_insert_scale_factor gauge
pg_settings_autovacuum_vacuum_insert_scale_factor{server="postgres:5432"} 0.2


# HELP pg_settings_autovacuum_vacuum_insert_threshold Server Parameter: autovacuum_vacuum_insert_threshold
# TYPE pg_settings_autovacuum_vacuum_insert_threshold gauge
pg_settings_autovacuum_vacuum_insert_threshold{server="postgres:5432"} 1000


# HELP pg_settings_autovacuum_vacuum_scale_factor Server Parameter: autovacuum_vacuum_scale_factor
# TYPE pg_settings_autovacuum_vacuum_scale_factor gauge
pg_settings_autovacuum_vacuum_scale_factor{server="postgres:5432"} 0.2


# HELP pg_settings_autovacuum_vacuum_threshold Server Parameter: autovacuum_vacuum_threshold
# TYPE pg_settings_autovacuum_vacuum_threshold gauge
pg_settings_autovacuum_vacuum_threshold{server="postgres:5432"} 50


# HELP pg_settings_autovacuum_work_mem_bytes Server Parameter: autovacuum_work_mem [Units converted to bytes.]
# TYPE pg_settings_autovacuum_work_mem_bytes gauge
pg_settings_autovacuum_work_mem_bytes{server="postgres:5432"} -1


# HELP pg_settings_backend_flush_after_bytes Server Parameter: backend_flush_after [Units converted to bytes.]
# TYPE pg_settings_backend_flush_after_bytes gauge
pg_settings_backend_flush_after_bytes{server="postgres:5432"} 0


# HELP pg_settings_bgwriter_delay_seconds Server Parameter: bgwriter_delay [Units converted to seconds.]
# TYPE pg_settings_bgwriter_delay_seconds gauge
pg_settings_bgwriter_delay_seconds{server="postgres:5432"} 0.2


# HELP pg_settings_bgwriter_flush_after_bytes Server Parameter: bgwriter_flush_after [Units converted to bytes.]
# TYPE pg_settings_bgwriter_flush_after_bytes gauge
pg_settings_bgwriter_flush_after_bytes{server="postgres:5432"} 524288


# HELP pg_settings_bgwriter_lru_maxpages Server Parameter: bgwriter_lru_maxpages
# TYPE pg_settings_bgwriter_lru_maxpages gauge
pg_settings_bgwriter_lru_maxpages{server="postgres:5432"} 100


# HELP pg_settings_bgwriter_lru_multiplier Server Parameter: bgwriter_lru_multiplier
# TYPE pg_settings_bgwriter_lru_multiplier gauge
pg_settings_bgwriter_lru_multiplier{server="postgres:5432"} 2


# HELP pg_settings_block_size Server Parameter: block_size
# TYPE pg_settings_block_size gauge
pg_settings_block_size{server="postgres:5432"} 8192


# HELP pg_settings_bonjour Server Parameter: bonjour
# TYPE pg_settings_bonjour gauge
pg_settings_bonjour{server="postgres:5432"} 0


# HELP pg_settings_check_function_bodies Server Parameter: check_function_bodies
# TYPE pg_settings_check_function_bodies gauge
pg_settings_check_function_bodies{server="postgres:5432"} 1


# HELP pg_settings_checkpoint_completion_target Server Parameter: checkpoint_completion_target
# TYPE pg_settings_checkpoint_completion_target gauge
pg_settings_checkpoint_completion_target{server="postgres:5432"} 0.9


# HELP pg_settings_checkpoint_flush_after_bytes Server Parameter: checkpoint_flush_after [Units converted to bytes.]
# TYPE pg_settings_checkpoint_flush_after_bytes gauge
pg_settings_checkpoint_flush_after_bytes{server="postgres:5432"} 262144


# HELP pg_settings_checkpoint_timeout_seconds Server Parameter: checkpoint_timeout [Units converted to seconds.]
# TYPE pg_settings_checkpoint_timeout_seconds gauge
pg_settings_checkpoint_timeout_seconds{server="postgres:5432"} 300


# HELP pg_settings_checkpoint_warning_seconds Server Parameter: checkpoint_warning [Units converted to seconds.]
# TYPE pg_settings_checkpoint_warning_seconds gauge
pg_settings_checkpoint_warning_seconds{server="postgres:5432"} 30


# HELP pg_settings_client_connection_check_interval_seconds Server Parameter: client_connection_check_interval [Units converted to seconds.]
# TYPE pg_settings_client_connection_check_interval_seconds gauge
pg_settings_client_connection_check_interval_seconds{server="postgres:5432"} 0


# HELP pg_settings_commit_delay Server Parameter: commit_delay
# TYPE pg_settings_commit_delay gauge
pg_settings_commit_delay{server="postgres:5432"} 0


# HELP pg_settings_commit_siblings Server Parameter: commit_siblings
# TYPE pg_settings_commit_siblings gauge
pg_settings_commit_siblings{server="postgres:5432"} 5


# HELP pg_settings_cpu_index_tuple_cost Server Parameter: cpu_index_tuple_cost
# TYPE pg_settings_cpu_index_tuple_cost gauge
pg_settings_cpu_index_tuple_cost{server="postgres:5432"} 0.005


# HELP pg_settings_cpu_operator_cost Server Parameter: cpu_operator_cost
# TYPE pg_settings_cpu_operator_cost gauge
pg_settings_cpu_operator_cost{server="postgres:5432"} 0.0025


# HELP pg_settings_cpu_tuple_cost Server Parameter: cpu_tuple_cost
# TYPE pg_settings_cpu_tuple_cost gauge
pg_settings_cpu_tuple_cost{server="postgres:5432"} 0.01


# HELP pg_settings_cursor_tuple_fraction Server Parameter: cursor_tuple_fraction
# TYPE pg_settings_cursor_tuple_fraction gauge
pg_settings_cursor_tuple_fraction{server="postgres:5432"} 0.1


# HELP pg_settings_data_checksums Server Parameter: data_checksums
# TYPE pg_settings_data_checksums gauge
pg_settings_data_checksums{server="postgres:5432"} 0


# HELP pg_settings_data_directory_mode Server Parameter: data_directory_mode
# TYPE pg_settings_data_directory_mode gauge
pg_settings_data_directory_mode{server="postgres:5432"} 700


# HELP pg_settings_data_sync_retry Server Parameter: data_sync_retry
# TYPE pg_settings_data_sync_retry gauge
pg_settings_data_sync_retry{server="postgres:5432"} 0


# HELP pg_settings_db_user_namespace Server Parameter: db_user_namespace
# TYPE pg_settings_db_user_namespace gauge
pg_settings_db_user_namespace{server="postgres:5432"} 0


# HELP pg_settings_deadlock_timeout_seconds Server Parameter: deadlock_timeout [Units converted to seconds.]
# TYPE pg_settings_deadlock_timeout_seconds gauge
pg_settings_deadlock_timeout_seconds{server="postgres:5432"} 1


# HELP pg_settings_debug_assertions Server Parameter: debug_assertions
# TYPE pg_settings_debug_assertions gauge
pg_settings_debug_assertions{server="postgres:5432"} 0


# HELP pg_settings_debug_discard_caches Server Parameter: debug_discard_caches
# TYPE pg_settings_debug_discard_caches gauge
pg_settings_debug_discard_caches{server="postgres:5432"} 0


# HELP pg_settings_debug_pretty_print Server Parameter: debug_pretty_print
# TYPE pg_settings_debug_pretty_print gauge
pg_settings_debug_pretty_print{server="postgres:5432"} 1


# HELP pg_settings_debug_print_parse Server Parameter: debug_print_parse
# TYPE pg_settings_debug_print_parse gauge
pg_settings_debug_print_parse{server="postgres:5432"} 0


# HELP pg_settings_debug_print_plan Server Parameter: debug_print_plan
# TYPE pg_settings_debug_print_plan gauge
pg_settings_debug_print_plan{server="postgres:5432"} 0


# HELP pg_settings_debug_print_rewritten Server Parameter: debug_print_rewritten
# TYPE pg_settings_debug_print_rewritten gauge
pg_settings_debug_print_rewritten{server="postgres:5432"} 0


# HELP pg_settings_default_statistics_target Server Parameter: default_statistics_target
# TYPE pg_settings_default_statistics_target gauge
pg_settings_default_statistics_target{server="postgres:5432"} 100


# HELP pg_settings_default_transaction_deferrable Server Parameter: default_transaction_deferrable
# TYPE pg_settings_default_transaction_deferrable gauge
pg_settings_default_transaction_deferrable{server="postgres:5432"} 0


# HELP pg_settings_default_transaction_read_only Server Parameter: default_transaction_read_only
# TYPE pg_settings_default_transaction_read_only gauge
pg_settings_default_transaction_read_only{server="postgres:5432"} 0


# HELP pg_settings_effective_cache_size_bytes Server Parameter: effective_cache_size [Units converted to bytes.]
# TYPE pg_settings_effective_cache_size_bytes gauge
pg_settings_effective_cache_size_bytes{server="postgres:5432"} 4.294967296e+09


# HELP pg_settings_effective_io_concurrency Server Parameter: effective_io_concurrency
# TYPE pg_settings_effective_io_concurrency gauge
pg_settings_effective_io_concurrency{server="postgres:5432"} 1


# HELP pg_settings_enable_async_append Server Parameter: enable_async_append
# TYPE pg_settings_enable_async_append gauge
pg_settings_enable_async_append{server="postgres:5432"} 1


# HELP pg_settings_enable_bitmapscan Server Parameter: enable_bitmapscan
# TYPE pg_settings_enable_bitmapscan gauge
pg_settings_enable_bitmapscan{server="postgres:5432"} 1


# HELP pg_settings_enable_gathermerge Server Parameter: enable_gathermerge
# TYPE pg_settings_enable_gathermerge gauge
pg_settings_enable_gathermerge{server="postgres:5432"} 1


# HELP pg_settings_enable_hashagg Server Parameter: enable_hashagg
# TYPE pg_settings_enable_hashagg gauge
pg_settings_enable_hashagg{server="postgres:5432"} 1


# HELP pg_settings_enable_hashjoin Server Parameter: enable_hashjoin
# TYPE pg_settings_enable_hashjoin gauge
pg_settings_enable_hashjoin{server="postgres:5432"} 1


# HELP pg_settings_enable_incremental_sort Server Parameter: enable_incremental_sort
# TYPE pg_settings_enable_incremental_sort gauge
pg_settings_enable_incremental_sort{server="postgres:5432"} 1


# HELP pg_settings_enable_indexonlyscan Server Parameter: enable_indexonlyscan
# TYPE pg_settings_enable_indexonlyscan gauge
pg_settings_enable_indexonlyscan{server="postgres:5432"} 1


# HELP pg_settings_enable_indexscan Server Parameter: enable_indexscan
# TYPE pg_settings_enable_indexscan gauge
pg_settings_enable_indexscan{server="postgres:5432"} 1


# HELP pg_settings_enable_material Server Parameter: enable_material
# TYPE pg_settings_enable_material gauge
pg_settings_enable_material{server="postgres:5432"} 1


# HELP pg_settings_enable_memoize Server Parameter: enable_memoize
# TYPE pg_settings_enable_memoize gauge
pg_settings_enable_memoize{server="postgres:5432"} 1


# HELP pg_settings_enable_mergejoin Server Parameter: enable_mergejoin
# TYPE pg_settings_enable_mergejoin gauge
pg_settings_enable_mergejoin{server="postgres:5432"} 1


# HELP pg_settings_enable_nestloop Server Parameter: enable_nestloop
# TYPE pg_settings_enable_nestloop gauge
pg_settings_enable_nestloop{server="postgres:5432"} 1


# HELP pg_settings_enable_parallel_append Server Parameter: enable_parallel_append
# TYPE pg_settings_enable_parallel_append gauge
pg_settings_enable_parallel_append{server="postgres:5432"} 1


# HELP pg_settings_enable_parallel_hash Server Parameter: enable_parallel_hash
# TYPE pg_settings_enable_parallel_hash gauge
pg_settings_enable_parallel_hash{server="postgres:5432"} 1


# HELP pg_settings_enable_partition_pruning Server Parameter: enable_partition_pruning
# TYPE pg_settings_enable_partition_pruning gauge
pg_settings_enable_partition_pruning{server="postgres:5432"} 1


# HELP pg_settings_enable_partitionwise_aggregate Server Parameter: enable_partitionwise_aggregate
# TYPE pg_settings_enable_partitionwise_aggregate gauge
pg_settings_enable_partitionwise_aggregate{server="postgres:5432"} 0


# HELP pg_settings_enable_partitionwise_join Server Parameter: enable_partitionwise_join
# TYPE pg_settings_enable_partitionwise_join gauge
pg_settings_enable_partitionwise_join{server="postgres:5432"} 0


# HELP pg_settings_enable_presorted_aggregate Server Parameter: enable_presorted_aggregate
# TYPE pg_settings_enable_presorted_aggregate gauge
pg_settings_enable_presorted_aggregate{server="postgres:5432"} 1


# HELP pg_settings_enable_seqscan Server Parameter: enable_seqscan
# TYPE pg_settings_enable_seqscan gauge
pg_settings_enable_seqscan{server="postgres:5432"} 1


# HELP pg_settings_enable_sort Server Parameter: enable_sort
# TYPE pg_settings_enable_sort gauge
pg_settings_enable_sort{server="postgres:5432"} 1


# HELP pg_settings_enable_tidscan Server Parameter: enable_tidscan
# TYPE pg_settings_enable_tidscan gauge
pg_settings_enable_tidscan{server="postgres:5432"} 1


# HELP pg_settings_escape_string_warning Server Parameter: escape_string_warning
# TYPE pg_settings_escape_string_warning gauge
pg_settings_escape_string_warning{server="postgres:5432"} 1


# HELP pg_settings_exit_on_error Server Parameter: exit_on_error
# TYPE pg_settings_exit_on_error gauge
pg_settings_exit_on_error{server="postgres:5432"} 0


# HELP pg_settings_extra_float_digits Server Parameter: extra_float_digits
# TYPE pg_settings_extra_float_digits gauge
pg_settings_extra_float_digits{server="postgres:5432"} 2


# HELP pg_settings_from_collapse_limit Server Parameter: from_collapse_limit
# TYPE pg_settings_from_collapse_limit gauge
pg_settings_from_collapse_limit{server="postgres:5432"} 8


# HELP pg_settings_fsync Server Parameter: fsync
# TYPE pg_settings_fsync gauge
pg_settings_fsync{server="postgres:5432"} 1


# HELP pg_settings_full_page_writes Server Parameter: full_page_writes
# TYPE pg_settings_full_page_writes gauge
pg_settings_full_page_writes{server="postgres:5432"} 1


# HELP pg_settings_geqo Server Parameter: geqo
# TYPE pg_settings_geqo gauge
pg_settings_geqo{server="postgres:5432"} 1


# HELP pg_settings_geqo_effort Server Parameter: geqo_effort
# TYPE pg_settings_geqo_effort gauge
pg_settings_geqo_effort{server="postgres:5432"} 5


# HELP pg_settings_geqo_generations Server Parameter: geqo_generations
# TYPE pg_settings_geqo_generations gauge
pg_settings_geqo_generations{server="postgres:5432"} 0


# HELP pg_settings_geqo_pool_size Server Parameter: geqo_pool_size
# TYPE pg_settings_geqo_pool_size gauge
pg_settings_geqo_pool_size{server="postgres:5432"} 0


# HELP pg_settings_geqo_seed Server Parameter: geqo_seed
# TYPE pg_settings_geqo_seed gauge
pg_settings_geqo_seed{server="postgres:5432"} 0


# HELP pg_settings_geqo_selection_bias Server Parameter: geqo_selection_bias
# TYPE pg_settings_geqo_selection_bias gauge
pg_settings_geqo_selection_bias{server="postgres:5432"} 2


# HELP pg_settings_geqo_threshold Server Parameter: geqo_threshold
# TYPE pg_settings_geqo_threshold gauge
pg_settings_geqo_threshold{server="postgres:5432"} 12


# HELP pg_settings_gin_fuzzy_search_limit Server Parameter: gin_fuzzy_search_limit
# TYPE pg_settings_gin_fuzzy_search_limit gauge
pg_settings_gin_fuzzy_search_limit{server="postgres:5432"} 0


# HELP pg_settings_gin_pending_list_limit_bytes Server Parameter: gin_pending_list_limit [Units converted to bytes.]
# TYPE pg_settings_gin_pending_list_limit_bytes gauge
pg_settings_gin_pending_list_limit_bytes{server="postgres:5432"} 4.194304e+06


# HELP pg_settings_gss_accept_delegation Server Parameter: gss_accept_delegation
# TYPE pg_settings_gss_accept_delegation gauge
pg_settings_gss_accept_delegation{server="postgres:5432"} 0


# HELP pg_settings_hash_mem_multiplier Server Parameter: hash_mem_multiplier
# TYPE pg_settings_hash_mem_multiplier gauge
pg_settings_hash_mem_multiplier{server="postgres:5432"} 2


# HELP pg_settings_hot_standby Server Parameter: hot_standby
# TYPE pg_settings_hot_standby gauge
pg_settings_hot_standby{server="postgres:5432"} 1


# HELP pg_settings_hot_standby_feedback Server Parameter: hot_standby_feedback
# TYPE pg_settings_hot_standby_feedback gauge
pg_settings_hot_standby_feedback{server="postgres:5432"} 0


# HELP pg_settings_huge_page_size_bytes Server Parameter: huge_page_size [Units converted to bytes.]
# TYPE pg_settings_huge_page_size_bytes gauge
pg_settings_huge_page_size_bytes{server="postgres:5432"} 0


# HELP pg_settings_idle_in_transaction_session_timeout_seconds Server Parameter: idle_in_transaction_session_timeout [Units converted to seconds.]
# TYPE pg_settings_idle_in_transaction_session_timeout_seconds gauge
pg_settings_idle_in_transaction_session_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_idle_session_timeout_seconds Server Parameter: idle_session_timeout [Units converted to seconds.]
# TYPE pg_settings_idle_session_timeout_seconds gauge
pg_settings_idle_session_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_ignore_checksum_failure Server Parameter: ignore_checksum_failure
# TYPE pg_settings_ignore_checksum_failure gauge
pg_settings_ignore_checksum_failure{server="postgres:5432"} 0


# HELP pg_settings_ignore_invalid_pages Server Parameter: ignore_invalid_pages
# TYPE pg_settings_ignore_invalid_pages gauge
pg_settings_ignore_invalid_pages{server="postgres:5432"} 0


# HELP pg_settings_ignore_system_indexes Server Parameter: ignore_system_indexes
# TYPE pg_settings_ignore_system_indexes gauge
pg_settings_ignore_system_indexes{server="postgres:5432"} 0


# HELP pg_settings_in_hot_standby Server Parameter: in_hot_standby
# TYPE pg_settings_in_hot_standby gauge
pg_settings_in_hot_standby{server="postgres:5432"} 0


# HELP pg_settings_integer_datetimes Server Parameter: integer_datetimes
# TYPE pg_settings_integer_datetimes gauge
pg_settings_integer_datetimes{server="postgres:5432"} 1


# HELP pg_settings_jit Server Parameter: jit
# TYPE pg_settings_jit gauge
pg_settings_jit{server="postgres:5432"} 1


# HELP pg_settings_jit_above_cost Server Parameter: jit_above_cost
# TYPE pg_settings_jit_above_cost gauge
pg_settings_jit_above_cost{server="postgres:5432"} 100000


# HELP pg_settings_jit_debugging_support Server Parameter: jit_debugging_support
# TYPE pg_settings_jit_debugging_support gauge
pg_settings_jit_debugging_support{server="postgres:5432"} 0


# HELP pg_settings_jit_dump_bitcode Server Parameter: jit_dump_bitcode
# TYPE pg_settings_jit_dump_bitcode gauge
pg_settings_jit_dump_bitcode{server="postgres:5432"} 0


# HELP pg_settings_jit_expressions Server Parameter: jit_expressions
# TYPE pg_settings_jit_expressions gauge
pg_settings_jit_expressions{server="postgres:5432"} 1


# HELP pg_settings_jit_inline_above_cost Server Parameter: jit_inline_above_cost
# TYPE pg_settings_jit_inline_above_cost gauge
pg_settings_jit_inline_above_cost{server="postgres:5432"} 500000


# HELP pg_settings_jit_optimize_above_cost Server Parameter: jit_optimize_above_cost
# TYPE pg_settings_jit_optimize_above_cost gauge
pg_settings_jit_optimize_above_cost{server="postgres:5432"} 500000


# HELP pg_settings_jit_profiling_support Server Parameter: jit_profiling_support
# TYPE pg_settings_jit_profiling_support gauge
pg_settings_jit_profiling_support{server="postgres:5432"} 0


# HELP pg_settings_jit_tuple_deforming Server Parameter: jit_tuple_deforming
# TYPE pg_settings_jit_tuple_deforming gauge
pg_settings_jit_tuple_deforming{server="postgres:5432"} 1


# HELP pg_settings_join_collapse_limit Server Parameter: join_collapse_limit
# TYPE pg_settings_join_collapse_limit gauge
pg_settings_join_collapse_limit{server="postgres:5432"} 8


# HELP pg_settings_krb_caseins_users Server Parameter: krb_caseins_users
# TYPE pg_settings_krb_caseins_users gauge
pg_settings_krb_caseins_users{server="postgres:5432"} 0


# HELP pg_settings_lo_compat_privileges Server Parameter: lo_compat_privileges
# TYPE pg_settings_lo_compat_privileges gauge
pg_settings_lo_compat_privileges{server="postgres:5432"} 0


# HELP pg_settings_lock_timeout_seconds Server Parameter: lock_timeout [Units converted to seconds.]
# TYPE pg_settings_lock_timeout_seconds gauge
pg_settings_lock_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_log_autovacuum_min_duration_seconds Server Parameter: log_autovacuum_min_duration [Units converted to seconds.]
# TYPE pg_settings_log_autovacuum_min_duration_seconds gauge
pg_settings_log_autovacuum_min_duration_seconds{server="postgres:5432"} 600


# HELP pg_settings_log_checkpoints Server Parameter: log_checkpoints
# TYPE pg_settings_log_checkpoints gauge
pg_settings_log_checkpoints{server="postgres:5432"} 1


# HELP pg_settings_log_connections Server Parameter: log_connections
# TYPE pg_settings_log_connections gauge
pg_settings_log_connections{server="postgres:5432"} 0


# HELP pg_settings_log_disconnections Server Parameter: log_disconnections
# TYPE pg_settings_log_disconnections gauge
pg_settings_log_disconnections{server="postgres:5432"} 0


# HELP pg_settings_log_duration Server Parameter: log_duration
# TYPE pg_settings_log_duration gauge
pg_settings_log_duration{server="postgres:5432"} 0


# HELP pg_settings_log_executor_stats Server Parameter: log_executor_stats
# TYPE pg_settings_log_executor_stats gauge
pg_settings_log_executor_stats{server="postgres:5432"} 0


# HELP pg_settings_log_file_mode Server Parameter: log_file_mode
# TYPE pg_settings_log_file_mode gauge
pg_settings_log_file_mode{server="postgres:5432"} 600


# HELP pg_settings_log_hostname Server Parameter: log_hostname
# TYPE pg_settings_log_hostname gauge
pg_settings_log_hostname{server="postgres:5432"} 0


# HELP pg_settings_log_lock_waits Server Parameter: log_lock_waits
# TYPE pg_settings_log_lock_waits gauge
pg_settings_log_lock_waits{server="postgres:5432"} 0


# HELP pg_settings_log_min_duration_sample_seconds Server Parameter: log_min_duration_sample [Units converted to seconds.]
# TYPE pg_settings_log_min_duration_sample_seconds gauge
pg_settings_log_min_duration_sample_seconds{server="postgres:5432"} -1


# HELP pg_settings_log_min_duration_statement_seconds Server Parameter: log_min_duration_statement [Units converted to seconds.]
# TYPE pg_settings_log_min_duration_statement_seconds gauge
pg_settings_log_min_duration_statement_seconds{server="postgres:5432"} -1


# HELP pg_settings_log_parameter_max_length_bytes Server Parameter: log_parameter_max_length [Units converted to bytes.]
# TYPE pg_settings_log_parameter_max_length_bytes gauge
pg_settings_log_parameter_max_length_bytes{server="postgres:5432"} -1


# HELP pg_settings_log_parameter_max_length_on_error_bytes Server Parameter: log_parameter_max_length_on_error [Units converted to bytes.]
# TYPE pg_settings_log_parameter_max_length_on_error_bytes gauge
pg_settings_log_parameter_max_length_on_error_bytes{server="postgres:5432"} 0


# HELP pg_settings_log_parser_stats Server Parameter: log_parser_stats
# TYPE pg_settings_log_parser_stats gauge
pg_settings_log_parser_stats{server="postgres:5432"} 0


# HELP pg_settings_log_planner_stats Server Parameter: log_planner_stats
# TYPE pg_settings_log_planner_stats gauge
pg_settings_log_planner_stats{server="postgres:5432"} 0


# HELP pg_settings_log_recovery_conflict_waits Server Parameter: log_recovery_conflict_waits
# TYPE pg_settings_log_recovery_conflict_waits gauge
pg_settings_log_recovery_conflict_waits{server="postgres:5432"} 0


# HELP pg_settings_log_replication_commands Server Parameter: log_replication_commands
# TYPE pg_settings_log_replication_commands gauge
pg_settings_log_replication_commands{server="postgres:5432"} 0


# HELP pg_settings_log_rotation_age_seconds Server Parameter: log_rotation_age [Units converted to seconds.]
# TYPE pg_settings_log_rotation_age_seconds gauge
pg_settings_log_rotation_age_seconds{server="postgres:5432"} 86400


# HELP pg_settings_log_rotation_size_bytes Server Parameter: log_rotation_size [Units converted to bytes.]
# TYPE pg_settings_log_rotation_size_bytes gauge
pg_settings_log_rotation_size_bytes{server="postgres:5432"} 1.048576e+07


# HELP pg_settings_log_startup_progress_interval_seconds Server Parameter: log_startup_progress_interval [Units converted to seconds.]
# TYPE pg_settings_log_startup_progress_interval_seconds gauge
pg_settings_log_startup_progress_interval_seconds{server="postgres:5432"} 10


# HELP pg_settings_log_statement_sample_rate Server Parameter: log_statement_sample_rate
# TYPE pg_settings_log_statement_sample_rate gauge
pg_settings_log_statement_sample_rate{server="postgres:5432"} 1


# HELP pg_settings_log_statement_stats Server Parameter: log_statement_stats
# TYPE pg_settings_log_statement_stats gauge
pg_settings_log_statement_stats{server="postgres:5432"} 0


# HELP pg_settings_log_temp_files_bytes Server Parameter: log_temp_files [Units converted to bytes.]
# TYPE pg_settings_log_temp_files_bytes gauge
pg_settings_log_temp_files_bytes{server="postgres:5432"} -1


# HELP pg_settings_log_transaction_sample_rate Server Parameter: log_transaction_sample_rate
# TYPE pg_settings_log_transaction_sample_rate gauge
pg_settings_log_transaction_sample_rate{server="postgres:5432"} 0


# HELP pg_settings_log_truncate_on_rotation Server Parameter: log_truncate_on_rotation
# TYPE pg_settings_log_truncate_on_rotation gauge
pg_settings_log_truncate_on_rotation{server="postgres:5432"} 0


# HELP pg_settings_logging_collector Server Parameter: logging_collector
# TYPE pg_settings_logging_collector gauge
pg_settings_logging_collector{server="postgres:5432"} 0


# HELP pg_settings_logical_decoding_work_mem_bytes Server Parameter: logical_decoding_work_mem [Units converted to bytes.]
# TYPE pg_settings_logical_decoding_work_mem_bytes gauge
pg_settings_logical_decoding_work_mem_bytes{server="postgres:5432"} 6.7108864e+07


# HELP pg_settings_maintenance_io_concurrency Server Parameter: maintenance_io_concurrency
# TYPE pg_settings_maintenance_io_concurrency gauge
pg_settings_maintenance_io_concurrency{server="postgres:5432"} 10


# HELP pg_settings_maintenance_work_mem_bytes Server Parameter: maintenance_work_mem [Units converted to bytes.]
# TYPE pg_settings_maintenance_work_mem_bytes gauge
pg_settings_maintenance_work_mem_bytes{server="postgres:5432"} 6.7108864e+07


# HELP pg_settings_max_connections Server Parameter: max_connections
# TYPE pg_settings_max_connections gauge
pg_settings_max_connections{server="postgres:5432"} 100


# HELP pg_settings_max_files_per_process Server Parameter: max_files_per_process
# TYPE pg_settings_max_files_per_process gauge
pg_settings_max_files_per_process{server="postgres:5432"} 1000


# HELP pg_settings_max_function_args Server Parameter: max_function_args
# TYPE pg_settings_max_function_args gauge
pg_settings_max_function_args{server="postgres:5432"} 100


# HELP pg_settings_max_identifier_length Server Parameter: max_identifier_length
# TYPE pg_settings_max_identifier_length gauge
pg_settings_max_identifier_length{server="postgres:5432"} 63


# HELP pg_settings_max_index_keys Server Parameter: max_index_keys
# TYPE pg_settings_max_index_keys gauge
pg_settings_max_index_keys{server="postgres:5432"} 32


# HELP pg_settings_max_locks_per_transaction Server Parameter: max_locks_per_transaction
# TYPE pg_settings_max_locks_per_transaction gauge
pg_settings_max_locks_per_transaction{server="postgres:5432"} 64


# HELP pg_settings_max_logical_replication_workers Server Parameter: max_logical_replication_workers
# TYPE pg_settings_max_logical_replication_workers gauge
pg_settings_max_logical_replication_workers{server="postgres:5432"} 4


# HELP pg_settings_max_parallel_apply_workers_per_subscription Server Parameter: max_parallel_apply_workers_per_subscription
# TYPE pg_settings_max_parallel_apply_workers_per_subscription gauge
pg_settings_max_parallel_apply_workers_per_subscription{server="postgres:5432"} 2


# HELP pg_settings_max_parallel_maintenance_workers Server Parameter: max_parallel_maintenance_workers
# TYPE pg_settings_max_parallel_maintenance_workers gauge
pg_settings_max_parallel_maintenance_workers{server="postgres:5432"} 2


# HELP pg_settings_max_parallel_workers Server Parameter: max_parallel_workers
# TYPE pg_settings_max_parallel_workers gauge
pg_settings_max_parallel_workers{server="postgres:5432"} 8


# HELP pg_settings_max_parallel_workers_per_gather Server Parameter: max_parallel_workers_per_gather
# TYPE pg_settings_max_parallel_workers_per_gather gauge
pg_settings_max_parallel_workers_per_gather{server="postgres:5432"} 2


# HELP pg_settings_max_pred_locks_per_page Server Parameter: max_pred_locks_per_page
# TYPE pg_settings_max_pred_locks_per_page gauge
pg_settings_max_pred_locks_per_page{server="postgres:5432"} 2


# HELP pg_settings_max_pred_locks_per_relation Server Parameter: max_pred_locks_per_relation
# TYPE pg_settings_max_pred_locks_per_relation gauge
pg_settings_max_pred_locks_per_relation{server="postgres:5432"} -2


# HELP pg_settings_max_pred_locks_per_transaction Server Parameter: max_pred_locks_per_transaction
# TYPE pg_settings_max_pred_locks_per_transaction gauge
pg_settings_max_pred_locks_per_transaction{server="postgres:5432"} 64


# HELP pg_settings_max_prepared_transactions Server Parameter: max_prepared_transactions
# TYPE pg_settings_max_prepared_transactions gauge
pg_settings_max_prepared_transactions{server="postgres:5432"} 0


# HELP pg_settings_max_replication_slots Server Parameter: max_replication_slots
# TYPE pg_settings_max_replication_slots gauge
pg_settings_max_replication_slots{server="postgres:5432"} 10


# HELP pg_settings_max_slot_wal_keep_size_bytes Server Parameter: max_slot_wal_keep_size [Units converted to bytes.]
# TYPE pg_settings_max_slot_wal_keep_size_bytes gauge
pg_settings_max_slot_wal_keep_size_bytes{server="postgres:5432"} -1


# HELP pg_settings_max_stack_depth_bytes Server Parameter: max_stack_depth [Units converted to bytes.]
# TYPE pg_settings_max_stack_depth_bytes gauge
pg_settings_max_stack_depth_bytes{server="postgres:5432"} 2.097152e+06


# HELP pg_settings_max_standby_archive_delay_seconds Server Parameter: max_standby_archive_delay [Units converted to seconds.]
# TYPE pg_settings_max_standby_archive_delay_seconds gauge
pg_settings_max_standby_archive_delay_seconds{server="postgres:5432"} 30


# HELP pg_settings_max_standby_streaming_delay_seconds Server Parameter: max_standby_streaming_delay [Units converted to seconds.]
# TYPE pg_settings_max_standby_streaming_delay_seconds gauge
pg_settings_max_standby_streaming_delay_seconds{server="postgres:5432"} 30


# HELP pg_settings_max_sync_workers_per_subscription Server Parameter: max_sync_workers_per_subscription
# TYPE pg_settings_max_sync_workers_per_subscription gauge
pg_settings_max_sync_workers_per_subscription{server="postgres:5432"} 2


# HELP pg_settings_max_wal_senders Server Parameter: max_wal_senders
# TYPE pg_settings_max_wal_senders gauge
pg_settings_max_wal_senders{server="postgres:5432"} 10


# HELP pg_settings_max_wal_size_bytes Server Parameter: max_wal_size [Units converted to bytes.]
# TYPE pg_settings_max_wal_size_bytes gauge
pg_settings_max_wal_size_bytes{server="postgres:5432"} 1.073741824e+09


# HELP pg_settings_max_worker_processes Server Parameter: max_worker_processes
# TYPE pg_settings_max_worker_processes gauge
pg_settings_max_worker_processes{server="postgres:5432"} 8


# HELP pg_settings_min_dynamic_shared_memory_bytes Server Parameter: min_dynamic_shared_memory [Units converted to bytes.]
# TYPE pg_settings_min_dynamic_shared_memory_bytes gauge
pg_settings_min_dynamic_shared_memory_bytes{server="postgres:5432"} 0


# HELP pg_settings_min_parallel_index_scan_size_bytes Server Parameter: min_parallel_index_scan_size [Units converted to bytes.]
# TYPE pg_settings_min_parallel_index_scan_size_bytes gauge
pg_settings_min_parallel_index_scan_size_bytes{server="postgres:5432"} 524288


# HELP pg_settings_min_parallel_table_scan_size_bytes Server Parameter: min_parallel_table_scan_size [Units converted to bytes.]
# TYPE pg_settings_min_parallel_table_scan_size_bytes gauge
pg_settings_min_parallel_table_scan_size_bytes{server="postgres:5432"} 8.388608e+06


# HELP pg_settings_min_wal_size_bytes Server Parameter: min_wal_size [Units converted to bytes.]
# TYPE pg_settings_min_wal_size_bytes gauge
pg_settings_min_wal_size_bytes{server="postgres:5432"} 8.388608e+07


# HELP pg_settings_old_snapshot_threshold_seconds Server Parameter: old_snapshot_threshold [Units converted to seconds.]
# TYPE pg_settings_old_snapshot_threshold_seconds gauge
pg_settings_old_snapshot_threshold_seconds{server="postgres:5432"} -1


# HELP pg_settings_parallel_leader_participation Server Parameter: parallel_leader_participation
# TYPE pg_settings_parallel_leader_participation gauge
pg_settings_parallel_leader_participation{server="postgres:5432"} 1


# HELP pg_settings_parallel_setup_cost Server Parameter: parallel_setup_cost
# TYPE pg_settings_parallel_setup_cost gauge
pg_settings_parallel_setup_cost{server="postgres:5432"} 1000


# HELP pg_settings_parallel_tuple_cost Server Parameter: parallel_tuple_cost
# TYPE pg_settings_parallel_tuple_cost gauge
pg_settings_parallel_tuple_cost{server="postgres:5432"} 0.1


# HELP pg_settings_port Server Parameter: port
# TYPE pg_settings_port gauge
pg_settings_port{server="postgres:5432"} 5432


# HELP pg_settings_post_auth_delay_seconds Server Parameter: post_auth_delay [Units converted to seconds.]
# TYPE pg_settings_post_auth_delay_seconds gauge
pg_settings_post_auth_delay_seconds{server="postgres:5432"} 0


# HELP pg_settings_pre_auth_delay_seconds Server Parameter: pre_auth_delay [Units converted to seconds.]
# TYPE pg_settings_pre_auth_delay_seconds gauge
pg_settings_pre_auth_delay_seconds{server="postgres:5432"} 0


# HELP pg_settings_quote_all_identifiers Server Parameter: quote_all_identifiers
# TYPE pg_settings_quote_all_identifiers gauge
pg_settings_quote_all_identifiers{server="postgres:5432"} 0


# HELP pg_settings_random_page_cost Server Parameter: random_page_cost
# TYPE pg_settings_random_page_cost gauge
pg_settings_random_page_cost{server="postgres:5432"} 4


# HELP pg_settings_recovery_min_apply_delay_seconds Server Parameter: recovery_min_apply_delay [Units converted to seconds.]
# TYPE pg_settings_recovery_min_apply_delay_seconds gauge
pg_settings_recovery_min_apply_delay_seconds{server="postgres:5432"} 0


# HELP pg_settings_recovery_target_inclusive Server Parameter: recovery_target_inclusive
# TYPE pg_settings_recovery_target_inclusive gauge
pg_settings_recovery_target_inclusive{server="postgres:5432"} 1


# HELP pg_settings_recursive_worktable_factor Server Parameter: recursive_worktable_factor
# TYPE pg_settings_recursive_worktable_factor gauge
pg_settings_recursive_worktable_factor{server="postgres:5432"} 10


# HELP pg_settings_remove_temp_files_after_crash Server Parameter: remove_temp_files_after_crash
# TYPE pg_settings_remove_temp_files_after_crash gauge
pg_settings_remove_temp_files_after_crash{server="postgres:5432"} 1


# HELP pg_settings_reserved_connections Server Parameter: reserved_connections
# TYPE pg_settings_reserved_connections gauge
pg_settings_reserved_connections{server="postgres:5432"} 0


# HELP pg_settings_restart_after_crash Server Parameter: restart_after_crash
# TYPE pg_settings_restart_after_crash gauge
pg_settings_restart_after_crash{server="postgres:5432"} 1


# HELP pg_settings_row_security Server Parameter: row_security
# TYPE pg_settings_row_security gauge
pg_settings_row_security{server="postgres:5432"} 1


# HELP pg_settings_scram_iterations Server Parameter: scram_iterations
# TYPE pg_settings_scram_iterations gauge
pg_settings_scram_iterations{server="postgres:5432"} 4096


# HELP pg_settings_segment_size_bytes Server Parameter: segment_size [Units converted to bytes.]
# TYPE pg_settings_segment_size_bytes gauge
pg_settings_segment_size_bytes{server="postgres:5432"} 1.073741824e+09


# HELP pg_settings_send_abort_for_crash Server Parameter: send_abort_for_crash
# TYPE pg_settings_send_abort_for_crash gauge
pg_settings_send_abort_for_crash{server="postgres:5432"} 0


# HELP pg_settings_send_abort_for_kill Server Parameter: send_abort_for_kill
# TYPE pg_settings_send_abort_for_kill gauge
pg_settings_send_abort_for_kill{server="postgres:5432"} 0


# HELP pg_settings_seq_page_cost Server Parameter: seq_page_cost
# TYPE pg_settings_seq_page_cost gauge
pg_settings_seq_page_cost{server="postgres:5432"} 1


# HELP pg_settings_server_version_num Server Parameter: server_version_num
# TYPE pg_settings_server_version_num gauge
pg_settings_server_version_num{server="postgres:5432"} 160009


# HELP pg_settings_shared_buffers_bytes Server Parameter: shared_buffers [Units converted to bytes.]
# TYPE pg_settings_shared_buffers_bytes gauge
pg_settings_shared_buffers_bytes{server="postgres:5432"} 1.34217728e+08


# HELP pg_settings_shared_memory_size_bytes Server Parameter: shared_memory_size [Units converted to bytes.]
# TYPE pg_settings_shared_memory_size_bytes gauge
pg_settings_shared_memory_size_bytes{server="postgres:5432"} 1.49946368e+08


# HELP pg_settings_shared_memory_size_in_huge_pages Server Parameter: shared_memory_size_in_huge_pages
# TYPE pg_settings_shared_memory_size_in_huge_pages gauge
pg_settings_shared_memory_size_in_huge_pages{server="postgres:5432"} 72


# HELP pg_settings_ssl Server Parameter: ssl
# TYPE pg_settings_ssl gauge
pg_settings_ssl{server="postgres:5432"} 0


# HELP pg_settings_ssl_passphrase_command_supports_reload Server Parameter: ssl_passphrase_command_supports_reload
# TYPE pg_settings_ssl_passphrase_command_supports_reload gauge
pg_settings_ssl_passphrase_command_supports_reload{server="postgres:5432"} 0


# HELP pg_settings_ssl_prefer_server_ciphers Server Parameter: ssl_prefer_server_ciphers
# TYPE pg_settings_ssl_prefer_server_ciphers gauge
pg_settings_ssl_prefer_server_ciphers{server="postgres:5432"} 1


# HELP pg_settings_standard_conforming_strings Server Parameter: standard_conforming_strings
# TYPE pg_settings_standard_conforming_strings gauge
pg_settings_standard_conforming_strings{server="postgres:5432"} 1


# HELP pg_settings_statement_timeout_seconds Server Parameter: statement_timeout [Units converted to seconds.]
# TYPE pg_settings_statement_timeout_seconds gauge
pg_settings_statement_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_superuser_reserved_connections Server Parameter: superuser_reserved_connections
# TYPE pg_settings_superuser_reserved_connections gauge
pg_settings_superuser_reserved_connections{server="postgres:5432"} 3


# HELP pg_settings_synchronize_seqscans Server Parameter: synchronize_seqscans
# TYPE pg_settings_synchronize_seqscans gauge
pg_settings_synchronize_seqscans{server="postgres:5432"} 1


# HELP pg_settings_syslog_sequence_numbers Server Parameter: syslog_sequence_numbers
# TYPE pg_settings_syslog_sequence_numbers gauge
pg_settings_syslog_sequence_numbers{server="postgres:5432"} 1


# HELP pg_settings_syslog_split_messages Server Parameter: syslog_split_messages
# TYPE pg_settings_syslog_split_messages gauge
pg_settings_syslog_split_messages{server="postgres:5432"} 1


# HELP pg_settings_tcp_keepalives_count Server Parameter: tcp_keepalives_count
# TYPE pg_settings_tcp_keepalives_count gauge
pg_settings_tcp_keepalives_count{server="postgres:5432"} 9


# HELP pg_settings_tcp_keepalives_idle_seconds Server Parameter: tcp_keepalives_idle [Units converted to seconds.]
# TYPE pg_settings_tcp_keepalives_idle_seconds gauge
pg_settings_tcp_keepalives_idle_seconds{server="postgres:5432"} 7200


# HELP pg_settings_tcp_keepalives_interval_seconds Server Parameter: tcp_keepalives_interval [Units converted to seconds.]
# TYPE pg_settings_tcp_keepalives_interval_seconds gauge
pg_settings_tcp_keepalives_interval_seconds{server="postgres:5432"} 75


# HELP pg_settings_tcp_user_timeout_seconds Server Parameter: tcp_user_timeout [Units converted to seconds.]
# TYPE pg_settings_tcp_user_timeout_seconds gauge
pg_settings_tcp_user_timeout_seconds{server="postgres:5432"} 0


# HELP pg_settings_temp_buffers_bytes Server Parameter: temp_buffers [Units converted to bytes.]
# TYPE pg_settings_temp_buffers_bytes gauge
pg_settings_temp_buffers_bytes{server="postgres:5432"} 8.388608e+06


# HELP pg_settings_temp_file_limit_bytes Server Parameter: temp_file_limit [Units converted to bytes.]
# TYPE pg_settings_temp_file_limit_bytes gauge
pg_settings_temp_file_limit_bytes{server="postgres:5432"} -1


# HELP pg_settings_trace_notify Server Parameter: trace_notify
# TYPE pg_settings_trace_notify gauge
pg_settings_trace_notify{server="postgres:5432"} 0


# HELP pg_settings_trace_sort Server Parameter: trace_sort
# TYPE pg_settings_trace_sort gauge
pg_settings_trace_sort{server="postgres:5432"} 0


# HELP pg_settings_track_activities Server Parameter: track_activities
# TYPE pg_settings_track_activities gauge
pg_settings_track_activities{server="postgres:5432"} 1


# HELP pg_settings_track_activity_query_size_bytes Server Parameter: track_activity_query_size [Units converted to bytes.]
# TYPE pg_settings_track_activity_query_size_bytes gauge
pg_settings_track_activity_query_size_bytes{server="postgres:5432"} 1024


# HELP pg_settings_track_commit_timestamp Server Parameter: track_commit_timestamp
# TYPE pg_settings_track_commit_timestamp gauge
pg_settings_track_commit_timestamp{server="postgres:5432"} 0


# HELP pg_settings_track_counts Server Parameter: track_counts
# TYPE pg_settings_track_counts gauge
pg_settings_track_counts{server="postgres:5432"} 1


# HELP pg_settings_track_io_timing Server Parameter: track_io_timing
# TYPE pg_settings_track_io_timing gauge
pg_settings_track_io_timing{server="postgres:5432"} 0


# HELP pg_settings_track_wal_io_timing Server Parameter: track_wal_io_timing
# TYPE pg_settings_track_wal_io_timing gauge
pg_settings_track_wal_io_timing{server="postgres:5432"} 0


# HELP pg_settings_transaction_deferrable Server Parameter: transaction_deferrable
# TYPE pg_settings_transaction_deferrable gauge
pg_settings_transaction_deferrable{server="postgres:5432"} 0


# HELP pg_settings_transaction_read_only Server Parameter: transaction_read_only
# TYPE pg_settings_transaction_read_only gauge
pg_settings_transaction_read_only{server="postgres:5432"} 0


# HELP pg_settings_transform_null_equals Server Parameter: transform_null_equals
# TYPE pg_settings_transform_null_equals gauge
pg_settings_transform_null_equals{server="postgres:5432"} 0


# HELP pg_settings_unix_socket_permissions Server Parameter: unix_socket_permissions
# TYPE pg_settings_unix_socket_permissions gauge
pg_settings_unix_socket_permissions{server="postgres:5432"} 777


# HELP pg_settings_update_process_title Server Parameter: update_process_title
# TYPE pg_settings_update_process_title gauge
pg_settings_update_process_title{server="postgres:5432"} 1


# HELP pg_settings_vacuum_buffer_usage_limit_bytes Server Parameter: vacuum_buffer_usage_limit [Units converted to bytes.]
# TYPE pg_settings_vacuum_buffer_usage_limit_bytes gauge
pg_settings_vacuum_buffer_usage_limit_bytes{server="postgres:5432"} 262144


# HELP pg_settings_vacuum_cost_delay_seconds Server Parameter: vacuum_cost_delay [Units converted to seconds.]
# TYPE pg_settings_vacuum_cost_delay_seconds gauge
pg_settings_vacuum_cost_delay_seconds{server="postgres:5432"} 0


# HELP pg_settings_vacuum_cost_limit Server Parameter: vacuum_cost_limit
# TYPE pg_settings_vacuum_cost_limit gauge
pg_settings_vacuum_cost_limit{server="postgres:5432"} 200


# HELP pg_settings_vacuum_cost_page_dirty Server Parameter: vacuum_cost_page_dirty
# TYPE pg_settings_vacuum_cost_page_dirty gauge
pg_settings_vacuum_cost_page_dirty{server="postgres:5432"} 20


# HELP pg_settings_vacuum_cost_page_hit Server Parameter: vacuum_cost_page_hit
# TYPE pg_settings_vacuum_cost_page_hit gauge
pg_settings_vacuum_cost_page_hit{server="postgres:5432"} 1


# HELP pg_settings_vacuum_cost_page_miss Server Parameter: vacuum_cost_page_miss
# TYPE pg_settings_vacuum_cost_page_miss gauge
pg_settings_vacuum_cost_page_miss{server="postgres:5432"} 2


# HELP pg_settings_vacuum_failsafe_age Server Parameter: vacuum_failsafe_age
# TYPE pg_settings_vacuum_failsafe_age gauge
pg_settings_vacuum_failsafe_age{server="postgres:5432"} 1.6e+09


# HELP pg_settings_vacuum_freeze_min_age Server Parameter: vacuum_freeze_min_age
# TYPE pg_settings_vacuum_freeze_min_age gauge
pg_settings_vacuum_freeze_min_age{server="postgres:5432"} 5e+07


# HELP pg_settings_vacuum_freeze_table_age Server Parameter: vacuum_freeze_table_age
# TYPE pg_settings_vacuum_freeze_table_age gauge
pg_settings_vacuum_freeze_table_age{server="postgres:5432"} 1.5e+08


# HELP pg_settings_vacuum_multixact_failsafe_age Server Parameter: vacuum_multixact_failsafe_age
# TYPE pg_settings_vacuum_multixact_failsafe_age gauge
pg_settings_vacuum_multixact_failsafe_age{server="postgres:5432"} 1.6e+09


# HELP pg_settings_vacuum_multixact_freeze_min_age Server Parameter: vacuum_multixact_freeze_min_age
# TYPE pg_settings_vacuum_multixact_freeze_min_age gauge
pg_settings_vacuum_multixact_freeze_min_age{server="postgres:5432"} 5e+06


# HELP pg_settings_vacuum_multixact_freeze_table_age Server Parameter: vacuum_multixact_freeze_table_age
# TYPE pg_settings_vacuum_multixact_freeze_table_age gauge
pg_settings_vacuum_multixact_freeze_table_age{server="postgres:5432"} 1.5e+08


# HELP pg_settings_wal_block_size Server Parameter: wal_block_size
# TYPE pg_settings_wal_block_size gauge
pg_settings_wal_block_size{server="postgres:5432"} 8192


# HELP pg_settings_wal_buffers_bytes Server Parameter: wal_buffers [Units converted to bytes.]
# TYPE pg_settings_wal_buffers_bytes gauge
pg_settings_wal_buffers_bytes{server="postgres:5432"} 4.194304e+06


# HELP pg_settings_wal_decode_buffer_size_bytes Server Parameter: wal_decode_buffer_size [Units converted to bytes.]
# TYPE pg_settings_wal_decode_buffer_size_bytes gauge
pg_settings_wal_decode_buffer_size_bytes{server="postgres:5432"} 524288


# HELP pg_settings_wal_init_zero Server Parameter: wal_init_zero
# TYPE pg_settings_wal_init_zero gauge
pg_settings_wal_init_zero{server="postgres:5432"} 1


# HELP pg_settings_wal_keep_size_bytes Server Parameter: wal_keep_size [Units converted to bytes.]
# TYPE pg_settings_wal_keep_size_bytes gauge
pg_settings_wal_keep_size_bytes{server="postgres:5432"} 0


# HELP pg_settings_wal_log_hints Server Parameter: wal_log_hints
# TYPE pg_settings_wal_log_hints gauge
pg_settings_wal_log_hints{server="postgres:5432"} 0


# HELP pg_settings_wal_receiver_create_temp_slot Server Parameter: wal_receiver_create_temp_slot
# TYPE pg_settings_wal_receiver_create_temp_slot gauge
pg_settings_wal_receiver_create_temp_slot{server="postgres:5432"} 0


# HELP pg_settings_wal_receiver_status_interval_seconds Server Parameter: wal_receiver_status_interval [Units converted to seconds.]
# TYPE pg_settings_wal_receiver_status_interval_seconds gauge
pg_settings_wal_receiver_status_interval_seconds{server="postgres:5432"} 10


# HELP pg_settings_wal_receiver_timeout_seconds Server Parameter: wal_receiver_timeout [Units converted to seconds.]
# TYPE pg_settings_wal_receiver_timeout_seconds gauge
pg_settings_wal_receiver_timeout_seconds{server="postgres:5432"} 60


# HELP pg_settings_wal_recycle Server Parameter: wal_recycle
# TYPE pg_settings_wal_recycle gauge
pg_settings_wal_recycle{server="postgres:5432"} 1


# HELP pg_settings_wal_retrieve_retry_interval_seconds Server Parameter: wal_retrieve_retry_interval [Units converted to seconds.]
# TYPE pg_settings_wal_retrieve_retry_interval_seconds gauge
pg_settings_wal_retrieve_retry_interval_seconds{server="postgres:5432"} 5


# HELP pg_settings_wal_segment_size_bytes Server Parameter: wal_segment_size [Units converted to bytes.]
# TYPE pg_settings_wal_segment_size_bytes gauge
pg_settings_wal_segment_size_bytes{server="postgres:5432"} 1.6777216e+07


# HELP pg_settings_wal_sender_timeout_seconds Server Parameter: wal_sender_timeout [Units converted to seconds.]
# TYPE pg_settings_wal_sender_timeout_seconds gauge
pg_settings_wal_sender_timeout_seconds{server="postgres:5432"} 60


# HELP pg_settings_wal_skip_threshold_bytes Server Parameter: wal_skip_threshold [Units converted to bytes.]
# TYPE pg_settings_wal_skip_threshold_bytes gauge
pg_settings_wal_skip_threshold_bytes{server="postgres:5432"} 2.097152e+06


# HELP pg_settings_wal_writer_delay_seconds Server Parameter: wal_writer_delay [Units converted to seconds.]
# TYPE pg_settings_wal_writer_delay_seconds gauge
pg_settings_wal_writer_delay_seconds{server="postgres:5432"} 0.2


# HELP pg_settings_wal_writer_flush_after_bytes Server Parameter: wal_writer_flush_after [Units converted to bytes.]
# TYPE pg_settings_wal_writer_flush_after_bytes gauge
pg_settings_wal_writer_flush_after_bytes{server="postgres:5432"} 1.048576e+06


# HELP pg_settings_work_mem_bytes Server Parameter: work_mem [Units converted to bytes.]
# TYPE pg_settings_work_mem_bytes gauge
pg_settings_work_mem_bytes{server="postgres:5432"} 4.194304e+06


# HELP pg_settings_zero_damaged_pages Server Parameter: zero_damaged_pages
# TYPE pg_settings_zero_damaged_pages gauge
pg_settings_zero_damaged_pages{server="postgres:5432"} 0


# HELP pg_stat_activity_count number of connections in this state
# TYPE pg_stat_activity_count gauge
pg_stat_activity_count{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_count{application_name="",backend_type="client backend",datname="francetravail",server="postgres:5432",state="active",usename="mhh",wait_event="",wait_event_type=""} 2
pg_stat_activity_count{application_name="",backend_type="client backend",datname="francetravail",server="postgres:5432",state="idle",usename="mhh",wait_event="ClientRead",wait_event_type="Client"} 44


# HELP pg_stat_activity_max_tx_duration max duration in seconds any active transaction has been running
# TYPE pg_stat_activity_max_tx_duration gauge
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="francetravail",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="postgres",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template0",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="active",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="disabled",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="fastpath function call",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle in transaction",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="",datname="template1",server="postgres:5432",state="idle in transaction (aborted)",usename="",wait_event="",wait_event_type=""} 0
pg_stat_activity_max_tx_duration{application_name="",backend_type="client backend",datname="francetravail",server="postgres:5432",state="active",usename="mhh",wait_event="",wait_event_type=""} 0.003473
pg_stat_activity_max_tx_duration{application_name="",backend_type="client backend",datname="francetravail",server="postgres:5432",state="idle",usename="mhh",wait_event="ClientRead",wait_event_type="Client"} 0


# HELP pg_stat_archiver_archived_count Number of WAL files that have been successfully archived
# TYPE pg_stat_archiver_archived_count counter
pg_stat_archiver_archived_count{server="postgres:5432"} 0


# HELP pg_stat_archiver_failed_count Number of failed attempts for archiving WAL files
# TYPE pg_stat_archiver_failed_count counter
pg_stat_archiver_failed_count{server="postgres:5432"} 0


# HELP pg_stat_archiver_last_archive_age Time in seconds since last WAL segment was successfully archived
# TYPE pg_stat_archiver_last_archive_age gauge
pg_stat_archiver_last_archive_age{server="postgres:5432"} NaN


# HELP pg_stat_bgwriter_buffers_alloc_total Number of buffers allocated
# TYPE pg_stat_bgwriter_buffers_alloc_total counter
pg_stat_bgwriter_buffers_alloc_total 68400


# HELP pg_stat_bgwriter_buffers_backend_fsync_total Number of times a backend had to execute its own fsync call (normally the background writer handles those even when the backend does its own write)
# TYPE pg_stat_bgwriter_buffers_backend_fsync_total counter
pg_stat_bgwriter_buffers_backend_fsync_total 0


# HELP pg_stat_bgwriter_buffers_backend_total Number of buffers written directly by a backend
# TYPE pg_stat_bgwriter_buffers_backend_total counter
pg_stat_bgwriter_buffers_backend_total 81654


# HELP pg_stat_bgwriter_buffers_checkpoint_total Number of buffers written during checkpoints
# TYPE pg_stat_bgwriter_buffers_checkpoint_total counter
pg_stat_bgwriter_buffers_checkpoint_total 48625


# HELP pg_stat_bgwriter_buffers_clean_total Number of buffers written by the background writer
# TYPE pg_stat_bgwriter_buffers_clean_total counter
pg_stat_bgwriter_buffers_clean_total 31907


# HELP pg_stat_bgwriter_checkpoint_sync_time_total Total amount of time that has been spent in the portion of checkpoint processing where files are synchronized to disk, in milliseconds
# TYPE pg_stat_bgwriter_checkpoint_sync_time_total counter
pg_stat_bgwriter_checkpoint_sync_time_total 7561


# HELP pg_stat_bgwriter_checkpoint_write_time_total Total amount of time that has been spent in the portion of checkpoint processing where files are written to disk, in milliseconds
# TYPE pg_stat_bgwriter_checkpoint_write_time_total counter
pg_stat_bgwriter_checkpoint_write_time_total 2.313599e+06


# HELP pg_stat_bgwriter_checkpoints_req_total Number of requested checkpoints that have been performed
# TYPE pg_stat_bgwriter_checkpoints_req_total counter
pg_stat_bgwriter_checkpoints_req_total 1


# HELP pg_stat_bgwriter_checkpoints_timed_total Number of scheduled checkpoints that have been performed
# TYPE pg_stat_bgwriter_checkpoints_timed_total counter
pg_stat_bgwriter_checkpoints_timed_total 73


# HELP pg_stat_bgwriter_maxwritten_clean_total Number of times the background writer stopped a cleaning scan because it had written too many buffers
# TYPE pg_stat_bgwriter_maxwritten_clean_total counter
pg_stat_bgwriter_maxwritten_clean_total 17


# HELP pg_stat_bgwriter_stats_reset_total Time at which these statistics were last reset
# TYPE pg_stat_bgwriter_stats_reset_total counter
pg_stat_bgwriter_stats_reset_total 1.751902367e+09


# HELP pg_stat_database_active_time_seconds_total Time spent executing SQL statements in this database, in seconds
# TYPE pg_stat_database_active_time_seconds_total counter
pg_stat_database_active_time_seconds_total{datid="1",datname="template1"} 0
pg_stat_database_active_time_seconds_total{datid="16384",datname="francetravail"} 4420.903928000001
pg_stat_database_active_time_seconds_total{datid="4",datname="template0"} 0
pg_stat_database_active_time_seconds_total{datid="5",datname="postgres"} 0.087755


# HELP pg_stat_database_blk_read_time Time spent reading data file blocks by backends in this database, in milliseconds
# TYPE pg_stat_database_blk_read_time counter
pg_stat_database_blk_read_time{datid="1",datname="template1"} 0
pg_stat_database_blk_read_time{datid="16384",datname="francetravail"} 0
pg_stat_database_blk_read_time{datid="4",datname="template0"} 0
pg_stat_database_blk_read_time{datid="5",datname="postgres"} 0


# HELP pg_stat_database_blk_write_time Time spent writing data file blocks by backends in this database, in milliseconds
# TYPE pg_stat_database_blk_write_time counter
pg_stat_database_blk_write_time{datid="1",datname="template1"} 0
pg_stat_database_blk_write_time{datid="16384",datname="francetravail"} 0
pg_stat_database_blk_write_time{datid="4",datname="template0"} 0
pg_stat_database_blk_write_time{datid="5",datname="postgres"} 0


# HELP pg_stat_database_blks_hit Number of times disk blocks were found already in the buffer cache, so that a read was not necessary (this only includes hits in the PostgreSQL buffer cache, not the operating system's file system cache)
# TYPE pg_stat_database_blks_hit counter
pg_stat_database_blks_hit{datid="1",datname="template1"} 115749
pg_stat_database_blks_hit{datid="16384",datname="francetravail"} 4.4165132e+07
pg_stat_database_blks_hit{datid="4",datname="template0"} 0
pg_stat_database_blks_hit{datid="5",datname="postgres"} 29704


# HELP pg_stat_database_blks_read Number of disk blocks read in this database
# TYPE pg_stat_database_blks_read counter
pg_stat_database_blks_read{datid="1",datname="template1"} 782
pg_stat_database_blks_read{datid="16384",datname="francetravail"} 81713
pg_stat_database_blks_read{datid="4",datname="template0"} 0
pg_stat_database_blks_read{datid="5",datname="postgres"} 208


# HELP pg_stat_database_conflicts Number of queries canceled due to conflicts with recovery in this database. (Conflicts occur only on standby servers; see pg_stat_database_conflicts for details.)
# TYPE pg_stat_database_conflicts counter
pg_stat_database_conflicts{datid="1",datname="template1"} 0
pg_stat_database_conflicts{datid="16384",datname="francetravail"} 0
pg_stat_database_conflicts{datid="4",datname="template0"} 0
pg_stat_database_conflicts{datid="5",datname="postgres"} 0


# HELP pg_stat_database_conflicts_confl_active_logicalslot Unknown metric from pg_stat_database_conflicts
# TYPE pg_stat_database_conflicts_confl_active_logicalslot untyped
pg_stat_database_conflicts_confl_active_logicalslot{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_active_logicalslot{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_active_logicalslot{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_active_logicalslot{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_conflicts_confl_bufferpin Number of queries in this database that have been canceled due to pinned buffers
# TYPE pg_stat_database_conflicts_confl_bufferpin counter
pg_stat_database_conflicts_confl_bufferpin{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_bufferpin{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_bufferpin{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_bufferpin{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_conflicts_confl_deadlock Number of queries in this database that have been canceled due to deadlocks
# TYPE pg_stat_database_conflicts_confl_deadlock counter
pg_stat_database_conflicts_confl_deadlock{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_deadlock{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_deadlock{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_deadlock{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_conflicts_confl_lock Number of queries in this database that have been canceled due to lock timeouts
# TYPE pg_stat_database_conflicts_confl_lock counter
pg_stat_database_conflicts_confl_lock{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_lock{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_lock{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_lock{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_conflicts_confl_snapshot Number of queries in this database that have been canceled due to old snapshots
# TYPE pg_stat_database_conflicts_confl_snapshot counter
pg_stat_database_conflicts_confl_snapshot{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_snapshot{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_snapshot{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_snapshot{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_conflicts_confl_tablespace Number of queries in this database that have been canceled due to dropped tablespaces
# TYPE pg_stat_database_conflicts_confl_tablespace counter
pg_stat_database_conflicts_confl_tablespace{datid="1",datname="template1",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_tablespace{datid="16384",datname="francetravail",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_tablespace{datid="4",datname="template0",server="postgres:5432"} 0
pg_stat_database_conflicts_confl_tablespace{datid="5",datname="postgres",server="postgres:5432"} 0


# HELP pg_stat_database_deadlocks Number of deadlocks detected in this database
# TYPE pg_stat_database_deadlocks counter
pg_stat_database_deadlocks{datid="1",datname="template1"} 0
pg_stat_database_deadlocks{datid="16384",datname="francetravail"} 0
pg_stat_database_deadlocks{datid="4",datname="template0"} 0
pg_stat_database_deadlocks{datid="5",datname="postgres"} 0


# HELP pg_stat_database_numbackends Number of backends currently connected to this database. This is the only column in this view that returns a value reflecting current state; all other columns return the accumulated values since the last reset.
# TYPE pg_stat_database_numbackends gauge
pg_stat_database_numbackends{datid="1",datname="template1"} 0
pg_stat_database_numbackends{datid="16384",datname="francetravail"} 46
pg_stat_database_numbackends{datid="4",datname="template0"} 0
pg_stat_database_numbackends{datid="5",datname="postgres"} 0


# HELP pg_stat_database_stats_reset Time at which these statistics were last reset
# TYPE pg_stat_database_stats_reset counter
pg_stat_database_stats_reset{datid="1",datname="template1"} 0
pg_stat_database_stats_reset{datid="16384",datname="francetravail"} 0
pg_stat_database_stats_reset{datid="4",datname="template0"} 0
pg_stat_database_stats_reset{datid="5",datname="postgres"} 0


# HELP pg_stat_database_temp_bytes Total amount of data written to temporary files by queries in this database. All temporary files are counted, regardless of why the temporary file was created, and regardless of the log_temp_files setting.
# TYPE pg_stat_database_temp_bytes counter
pg_stat_database_temp_bytes{datid="1",datname="template1"} 0
pg_stat_database_temp_bytes{datid="16384",datname="francetravail"} 4.620288e+06
pg_stat_database_temp_bytes{datid="4",datname="template0"} 0
pg_stat_database_temp_bytes{datid="5",datname="postgres"} 0


# HELP pg_stat_database_temp_files Number of temporary files created by queries in this database. All temporary files are counted, regardless of why the temporary file was created (e.g., sorting or hashing), and regardless of the log_temp_files setting.
# TYPE pg_stat_database_temp_files counter
pg_stat_database_temp_files{datid="1",datname="template1"} 0
pg_stat_database_temp_files{datid="16384",datname="francetravail"} 2
pg_stat_database_temp_files{datid="4",datname="template0"} 0
pg_stat_database_temp_files{datid="5",datname="postgres"} 0


# HELP pg_stat_database_tup_deleted Number of rows deleted by queries in this database
# TYPE pg_stat_database_tup_deleted counter
pg_stat_database_tup_deleted{datid="1",datname="template1"} 32
pg_stat_database_tup_deleted{datid="16384",datname="francetravail"} 134371
pg_stat_database_tup_deleted{datid="4",datname="template0"} 0
pg_stat_database_tup_deleted{datid="5",datname="postgres"} 0


# HELP pg_stat_database_tup_fetched Number of rows fetched by queries in this database
# TYPE pg_stat_database_tup_fetched counter
pg_stat_database_tup_fetched{datid="1",datname="template1"} 31275
pg_stat_database_tup_fetched{datid="16384",datname="francetravail"} 1.0638879e+07
pg_stat_database_tup_fetched{datid="4",datname="template0"} 0
pg_stat_database_tup_fetched{datid="5",datname="postgres"} 6665


# HELP pg_stat_database_tup_inserted Number of rows inserted by queries in this database
# TYPE pg_stat_database_tup_inserted counter
pg_stat_database_tup_inserted{datid="1",datname="template1"} 17735
pg_stat_database_tup_inserted{datid="16384",datname="francetravail"} 1.279239e+06
pg_stat_database_tup_inserted{datid="4",datname="template0"} 0
pg_stat_database_tup_inserted{datid="5",datname="postgres"} 0


# HELP pg_stat_database_tup_returned Number of rows returned by queries in this database
# TYPE pg_stat_database_tup_returned counter
pg_stat_database_tup_returned{datid="1",datname="template1"} 397266
pg_stat_database_tup_returned{datid="16384",datname="francetravail"} 2.5714759e+07
pg_stat_database_tup_returned{datid="4",datname="template0"} 0
pg_stat_database_tup_returned{datid="5",datname="postgres"} 325016


# HELP pg_stat_database_tup_updated Number of rows updated by queries in this database
# TYPE pg_stat_database_tup_updated counter
pg_stat_database_tup_updated{datid="1",datname="template1"} 712
pg_stat_database_tup_updated{datid="16384",datname="francetravail"} 92263
pg_stat_database_tup_updated{datid="4",datname="template0"} 0
pg_stat_database_tup_updated{datid="5",datname="postgres"} 0


# HELP pg_stat_database_xact_commit Number of transactions in this database that have been committed
# TYPE pg_stat_database_xact_commit counter
pg_stat_database_xact_commit{datid="1",datname="template1"} 1638
pg_stat_database_xact_commit{datid="16384",datname="francetravail"} 1.193426e+06
pg_stat_database_xact_commit{datid="4",datname="template0"} 0
pg_stat_database_xact_commit{datid="5",datname="postgres"} 738


# HELP pg_stat_database_xact_rollback Number of transactions in this database that have been rolled back
# TYPE pg_stat_database_xact_rollback counter
pg_stat_database_xact_rollback{datid="1",datname="template1"} 0
pg_stat_database_xact_rollback{datid="16384",datname="francetravail"} 11153
pg_stat_database_xact_rollback{datid="4",datname="template0"} 0
pg_stat_database_xact_rollback{datid="5",datname="postgres"} 0


# HELP pg_stat_user_tables_analyze_count Number of times this table has been manually analyzed
# TYPE pg_stat_user_tables_analyze_count counter
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="descriptionoffre",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_analyze_count{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_autoanalyze_count Number of times this table has been analyzed by the autovacuum daemon
# TYPE pg_stat_user_tables_autoanalyze_count counter
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_permission_view",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="ab_view_menu",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 9
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="competence",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="contrat",schemaname="public"} 2
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag",schemaname="public"} 110
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_bundle",schemaname="public"} 71
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_run",schemaname="public"} 41
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="entreprise",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="experience",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="formation",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="job",schemaname="public"} 179
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="localisation",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_competence",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_experience",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_formation",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_langue",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_qualification",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="offreemploi",schemaname="public"} 1
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 3
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="serialized_dag",schemaname="public"} 6
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_instance",schemaname="public"} 39
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_autoanalyze_count{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_autovacuum_count Number of times this table has been vacuumed by the autovacuum daemon
# TYPE pg_stat_user_tables_autovacuum_count counter
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="competence",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="contrat",schemaname="public"} 2
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag",schemaname="public"} 8
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_bundle",schemaname="public"} 76
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_run",schemaname="public"} 18
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="entreprise",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="formation",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="job",schemaname="public"} 189
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="localisation",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_competence",schemaname="public"} 2
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_experience",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_formation",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_langue",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_qualification",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="offreemploi",schemaname="public"} 1
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_instance",schemaname="public"} 48
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_autovacuum_count{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_idx_scan Number of index scans initiated on this table
# TYPE pg_stat_user_tables_idx_scan counter
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_permission",schemaname="public"} 24626
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_permission_view",schemaname="public"} 3273
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 569
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_role",schemaname="public"} 438
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_user",schemaname="public"} 186
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_user_role",schemaname="public"} 92
pg_stat_user_tables_idx_scan{datname="francetravail",relname="ab_view_menu",schemaname="public"} 19566
pg_stat_user_tables_idx_scan{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_event",schemaname="public"} 2
pg_stat_user_tables_idx_scan{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 2907
pg_stat_user_tables_idx_scan{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 71
pg_stat_user_tables_idx_scan{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="competence",schemaname="public"} 126540
pg_stat_user_tables_idx_scan{datname="francetravail",relname="connection",schemaname="public"} 26
pg_stat_user_tables_idx_scan{datname="francetravail",relname="contrat",schemaname="public"} 77716
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag",schemaname="public"} 413146
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_bundle",schemaname="public"} 114
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 6361
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_run",schemaname="public"} 241858
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_run_note",schemaname="public"} 35
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 12729
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 5
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 12729
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 5
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_tag",schemaname="public"} 12772
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_version",schemaname="public"} 11068
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dag_warning",schemaname="public"} 6391
pg_stat_user_tables_idx_scan{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 222
pg_stat_user_tables_idx_scan{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="descriptionoffre",schemaname="public"} 79630
pg_stat_user_tables_idx_scan{datname="francetravail",relname="entreprise",schemaname="public"} 77716
pg_stat_user_tables_idx_scan{datname="francetravail",relname="experience",schemaname="public"} 153985
pg_stat_user_tables_idx_scan{datname="francetravail",relname="formation",schemaname="public"} 5210
pg_stat_user_tables_idx_scan{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="job",schemaname="public"} 305
pg_stat_user_tables_idx_scan{datname="francetravail",relname="langue",schemaname="public"} 7108
pg_stat_user_tables_idx_scan{datname="francetravail",relname="localisation",schemaname="public"} 77716
pg_stat_user_tables_idx_scan{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="log_template",schemaname="public"} 21
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_competence",schemaname="public"} 60716
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_experience",schemaname="public"} 76667
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_formation",schemaname="public"} 1968
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_langue",schemaname="public"} 3539
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2561
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_qualification",schemaname="public"} 23690
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 24748
pg_stat_user_tables_idx_scan{datname="francetravail",relname="offreemploi",schemaname="public"} 271598
pg_stat_user_tables_idx_scan{datname="francetravail",relname="permisconduire",schemaname="public"} 5138
pg_stat_user_tables_idx_scan{datname="francetravail",relname="qualification",schemaname="public"} 23698
pg_stat_user_tables_idx_scan{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 49517
pg_stat_user_tables_idx_scan{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 556
pg_stat_user_tables_idx_scan{datname="francetravail",relname="serialized_dag",schemaname="public"} 50
pg_stat_user_tables_idx_scan{datname="francetravail",relname="session",schemaname="public"} 94
pg_stat_user_tables_idx_scan{datname="francetravail",relname="slot_pool",schemaname="public"} 4
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_instance",schemaname="public"} 200208
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_instance_history",schemaname="public"} 2940
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_instance_note",schemaname="public"} 31
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_map",schemaname="public"} 2370
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 12729
pg_stat_user_tables_idx_scan{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_idx_scan{datname="francetravail",relname="xcom",schemaname="public"} 684


# HELP pg_stat_user_tables_idx_tup_fetch Number of live rows fetched by index scans
# TYPE pg_stat_user_tables_idx_tup_fetch counter
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_permission",schemaname="public"} 24613
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_permission_view",schemaname="public"} 3202
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 2805
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_role",schemaname="public"} 433
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_user",schemaname="public"} 185
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_user_role",schemaname="public"} 92
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="ab_view_menu",schemaname="public"} 19473
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 44
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="competence",schemaname="public"} 121458
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="connection",schemaname="public"} 25
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag",schemaname="public"} 413092
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_bundle",schemaname="public"} 114
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_run",schemaname="public"} 194365
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_tag",schemaname="public"} 12772
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_version",schemaname="public"} 137060
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1914
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="experience",schemaname="public"} 153347
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="formation",schemaname="public"} 3954
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="job",schemaname="public"} 293
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="langue",schemaname="public"} 7076
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="log_template",schemaname="public"} 20
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_competence",schemaname="public"} 60715
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_experience",schemaname="public"} 76666
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_formation",schemaname="public"} 1967
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_langue",schemaname="public"} 3538
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2560
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_qualification",schemaname="public"} 23689
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 24747
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="offreemploi",schemaname="public"} 193882
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="permisconduire",schemaname="public"} 5120
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="qualification",schemaname="public"} 23689
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 49494
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 3065
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="serialized_dag",schemaname="public"} 50
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="session",schemaname="public"} 88
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="slot_pool",schemaname="public"} 3
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_instance",schemaname="public"} 183982
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_map",schemaname="public"} 2360
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_idx_tup_fetch{datname="francetravail",relname="xcom",schemaname="public"} 2958


# HELP pg_stat_user_tables_last_analyze Last time at which this table was manually analyzed
# TYPE pg_stat_user_tables_last_analyze gauge
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="descriptionoffre",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_last_analyze{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_last_autoanalyze Last time at which this table was analyzed by the autovacuum daemon
# TYPE pg_stat_user_tables_last_autoanalyze gauge
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_permission_view",schemaname="public"} 1.751902461e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 1.751902461e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="ab_view_menu",schemaname="public"} 1.751903002e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 1.751918996e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="competence",schemaname="public"} 1.751918997e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="contrat",schemaname="public"} 1.751919478e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag",schemaname="public"} 1.751935048e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_bundle",schemaname="public"} 1.751935048e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_run",schemaname="public"} 1.751919416e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1.751918943e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="entreprise",schemaname="public"} 1.751918881e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="experience",schemaname="public"} 1.751918997e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="formation",schemaname="public"} 1.751918998e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="job",schemaname="public"} 1.751935048e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="localisation",schemaname="public"} 1.751918885e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_competence",schemaname="public"} 1.751919356e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_experience",schemaname="public"} 1.751919417e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_formation",schemaname="public"} 1.751918998e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_langue",schemaname="public"} 1.751919056e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 1.751919056e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_qualification",schemaname="public"} 1.751919177e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 1.751919176e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="offreemploi",schemaname="public"} 1.751918886e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 1.751918996e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="serialized_dag",schemaname="public"} 1.75193274e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_instance",schemaname="public"} 1.751919476e+09
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_last_autoanalyze{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_last_autovacuum Last time at which this table was vacuumed by the autovacuum daemon
# TYPE pg_stat_user_tables_last_autovacuum gauge
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="competence",schemaname="public"} 1.751918997e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="contrat",schemaname="public"} 1.751919477e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag",schemaname="public"} 1.751919356e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_bundle",schemaname="public"} 1.751935048e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_run",schemaname="public"} 1.751919356e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1.751918941e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="entreprise",schemaname="public"} 1.751918877e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="formation",schemaname="public"} 1.751918998e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="job",schemaname="public"} 1.751935108e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="localisation",schemaname="public"} 1.751918882e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_competence",schemaname="public"} 1.751919416e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_experience",schemaname="public"} 1.751919416e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_formation",schemaname="public"} 1.751918998e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_langue",schemaname="public"} 1.751919056e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 1.751919056e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_qualification",schemaname="public"} 1.751919176e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 1.751919176e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="offreemploi",schemaname="public"} 1.751918885e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_instance",schemaname="public"} 1.751919416e+09
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_last_autovacuum{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_last_vacuum Last time at which this table was manually vacuumed (not counting VACUUM FULL)
# TYPE pg_stat_user_tables_last_vacuum gauge
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="descriptionoffre",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_last_vacuum{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_n_dead_tup Estimated number of dead rows
# TYPE pg_stat_user_tables_n_dead_tup gauge
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 3
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag",schemaname="public"} 36
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_bundle",schemaname="public"} 19
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_run",schemaname="public"} 12
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="descriptionoffre",schemaname="public"} 3657
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="job",schemaname="public"} 28
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_formation",schemaname="public"} 201
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="serialized_dag",schemaname="public"} 5
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="session",schemaname="public"} 31
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_instance",schemaname="public"} 35
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_dead_tup{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_n_live_tup Estimated number of live rows
# TYPE pg_stat_user_tables_n_live_tup gauge
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_permission",schemaname="public"} 5
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_permission_view",schemaname="public"} 110
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 242
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_role",schemaname="public"} 5
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_user",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_user_role",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="ab_view_menu",schemaname="public"} 54
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="alembic_version",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 218
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="competence",schemaname="public"} 5082
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="connection",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="contrat",schemaname="public"} 77716
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag",schemaname="public"} 2
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_bundle",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_code",schemaname="public"} 44
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_run",schemaname="public"} 4
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_tag",schemaname="public"} 2
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_version",schemaname="public"} 44
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="descriptionoffre",schemaname="public"} 77716
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="entreprise",schemaname="public"} 77716
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="experience",schemaname="public"} 707
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="formation",schemaname="public"} 2903
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="job",schemaname="public"} 3
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="langue",schemaname="public"} 32
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="localisation",schemaname="public"} 77716
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="log",schemaname="public"} 24
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="log_template",schemaname="public"} 2
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_competence",schemaname="public"} 11810
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_experience",schemaname="public"} 76666
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_formation",schemaname="public"} 1766
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_langue",schemaname="public"} 2940
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2522
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_qualification",schemaname="public"} 23689
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 8519
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="offreemploi",schemaname="public"} 77716
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="permisconduire",schemaname="public"} 18
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="qualification",schemaname="public"} 9
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 23
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 218
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="serialized_dag",schemaname="public"} 44
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="session",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="slot_pool",schemaname="public"} 1
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_instance",schemaname="public"} 222
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_map",schemaname="public"} 2
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_live_tup{datname="francetravail",relname="xcom",schemaname="public"} 28


# HELP pg_stat_user_tables_n_mod_since_analyze Estimated number of rows changed since last analyze
# TYPE pg_stat_user_tables_n_mod_since_analyze gauge
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_permission",schemaname="public"} 5
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_permission_view",schemaname="public"} 14
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_role",schemaname="public"} 5
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_user",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_user_role",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="alembic_version",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 21
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="connection",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag",schemaname="public"} 34
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_bundle",schemaname="public"} 19
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_code",schemaname="public"} 44
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_run",schemaname="public"} 33
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_tag",schemaname="public"} 2
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_version",schemaname="public"} 44
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="descriptionoffre",schemaname="public"} 4088
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="job",schemaname="public"} 61
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="langue",schemaname="public"} 32
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="log",schemaname="public"} 24
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="log_template",schemaname="public"} 2
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="permisconduire",schemaname="public"} 18
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="qualification",schemaname="public"} 9
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 23
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 5
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="serialized_dag",schemaname="public"} 41
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="session",schemaname="public"} 31
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="slot_pool",schemaname="public"} 1
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_map",schemaname="public"} 2
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_mod_since_analyze{datname="francetravail",relname="xcom",schemaname="public"} 28


# HELP pg_stat_user_tables_n_tup_del Number of rows deleted
# TYPE pg_stat_user_tables_n_tup_del counter
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="descriptionoffre",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_competence",schemaname="public"} 48905
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_formation",schemaname="public"} 201
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_langue",schemaname="public"} 598
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 38
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 16228
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_tup_del{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_n_tup_hot_upd Number of rows HOT updated (i.e., with no separate index update required)
# TYPE pg_stat_user_tables_n_tup_hot_upd counter
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 435
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="contrat",schemaname="public"} 9
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag",schemaname="public"} 6348
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_bundle",schemaname="public"} 3948
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_run",schemaname="public"} 2867
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="descriptionoffre",schemaname="public"} 958
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="serialized_dag",schemaname="public"} 322
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="session",schemaname="public"} 30
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_instance",schemaname="public"} 980
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_tup_hot_upd{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_n_tup_ins Number of rows inserted
# TYPE pg_stat_user_tables_n_tup_ins counter
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_permission",schemaname="public"} 5
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_permission_view",schemaname="public"} 110
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 242
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_role",schemaname="public"} 5
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_user",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_user_role",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="ab_view_menu",schemaname="public"} 54
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="alembic_version",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 218
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="competence",schemaname="public"} 5082
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="connection",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="contrat",schemaname="public"} 77716
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag",schemaname="public"} 2
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_bundle",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_code",schemaname="public"} 44
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_run",schemaname="public"} 4
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_tag",schemaname="public"} 2
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_version",schemaname="public"} 44
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="descriptionoffre",schemaname="public"} 77716
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="entreprise",schemaname="public"} 77716
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="experience",schemaname="public"} 707
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="formation",schemaname="public"} 2903
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="job",schemaname="public"} 3
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="langue",schemaname="public"} 32
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="localisation",schemaname="public"} 77716
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="log",schemaname="public"} 24
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="log_template",schemaname="public"} 2
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_competence",schemaname="public"} 60715
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_experience",schemaname="public"} 76666
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_formation",schemaname="public"} 1967
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_langue",schemaname="public"} 3538
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2560
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_qualification",schemaname="public"} 23689
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 24747
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="offreemploi",schemaname="public"} 77716
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="permisconduire",schemaname="public"} 18
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="qualification",schemaname="public"} 9
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 23
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 218
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="serialized_dag",schemaname="public"} 44
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="session",schemaname="public"} 2
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="slot_pool",schemaname="public"} 1
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_instance",schemaname="public"} 222
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_map",schemaname="public"} 2
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_tup_ins{datname="francetravail",relname="xcom",schemaname="public"} 28


# HELP pg_stat_user_tables_n_tup_upd Number of rows updated
# TYPE pg_stat_user_tables_n_tup_upd counter
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 436
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="contrat",schemaname="public"} 22067
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag",schemaname="public"} 6365
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_bundle",schemaname="public"} 3948
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_run",schemaname="public"} 2907
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="descriptionoffre",schemaname="public"} 4088
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="job",schemaname="public"} 12218
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="serialized_dag",schemaname="public"} 322
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="session",schemaname="public"} 30
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_instance",schemaname="public"} 5967
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_n_tup_upd{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_seq_scan Number of sequential scans initiated on this table
# TYPE pg_stat_user_tables_seq_scan counter
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_group",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_group_role",schemaname="public"} 4
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_permission",schemaname="public"} 46
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_permission_view",schemaname="public"} 3061
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 274
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_register_user",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_role",schemaname="public"} 110
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_user",schemaname="public"} 12
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_user_group",schemaname="public"} 4
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_user_role",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="ab_view_menu",schemaname="public"} 5485
pg_stat_user_tables_seq_scan{datname="francetravail",relname="alembic_version",schemaname="public"} 19
pg_stat_user_tables_seq_scan{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 4
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset",schemaname="public"} 10493
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_active",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_alias",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 21883
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_event",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="asset_trigger",schemaname="public"} 21539
pg_stat_user_tables_seq_scan{datname="francetravail",relname="backfill",schemaname="public"} 714
pg_stat_user_tables_seq_scan{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="callback_request",schemaname="public"} 105126
pg_stat_user_tables_seq_scan{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 3704
pg_stat_user_tables_seq_scan{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="competence",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="connection",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="contrat",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag",schemaname="public"} 181774
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_bundle",schemaname="public"} 7786
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_code",schemaname="public"} 6321
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 105127
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_run",schemaname="public"} 50799
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_run_note",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 47
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 47
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 47
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 47
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_tag",schemaname="public"} 10
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_version",schemaname="public"} 34
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dag_warning",schemaname="public"} 982
pg_stat_user_tables_seq_scan{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="deadline",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="descriptionoffre",schemaname="public"} 5
pg_stat_user_tables_seq_scan{datname="francetravail",relname="entreprise",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="experience",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="formation",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="import_error",schemaname="public"} 16683
pg_stat_user_tables_seq_scan{datname="francetravail",relname="job",schemaname="public"} 26120
pg_stat_user_tables_seq_scan{datname="francetravail",relname="langue",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="localisation",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="log",schemaname="public"} 4
pg_stat_user_tables_seq_scan{datname="francetravail",relname="log_template",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_competence",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_experience",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_formation",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_langue",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_qualification",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="offreemploi",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="permisconduire",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="qualification",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 151
pg_stat_user_tables_seq_scan{datname="francetravail",relname="serialized_dag",schemaname="public"} 12139
pg_stat_user_tables_seq_scan{datname="francetravail",relname="session",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="slot_pool",schemaname="public"} 26011
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_instance",schemaname="public"} 56519
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_instance_history",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_instance_note",schemaname="public"} 3
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_map",schemaname="public"} 1
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 47
pg_stat_user_tables_seq_scan{datname="francetravail",relname="task_reschedule",schemaname="public"} 225
pg_stat_user_tables_seq_scan{datname="francetravail",relname="trigger",schemaname="public"} 107680
pg_stat_user_tables_seq_scan{datname="francetravail",relname="variable",schemaname="public"} 2
pg_stat_user_tables_seq_scan{datname="francetravail",relname="xcom",schemaname="public"} 3


# HELP pg_stat_user_tables_seq_tup_read Number of live rows fetched by sequential scans
# TYPE pg_stat_user_tables_seq_tup_read counter
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_permission",schemaname="public"} 214
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_permission_view",schemaname="public"} 331274
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 65565
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_role",schemaname="public"} 536
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_user",schemaname="public"} 7
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="ab_view_menu",schemaname="public"} 287664
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="alembic_version",schemaname="public"} 18
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 3
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 462183
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="contrat",schemaname="public"} 155432
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag",schemaname="public"} 359999
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_bundle",schemaname="public"} 7784
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_code",schemaname="public"} 253683
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_run",schemaname="public"} 139612
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_tag",schemaname="public"} 16
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_version",schemaname="public"} 359
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="descriptionoffre",schemaname="public"} 310864
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="job",schemaname="public"} 78348
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_competence",schemaname="public"} 60715
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_experience",schemaname="public"} 76666
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_formation",schemaname="public"} 1967
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_langue",schemaname="public"} 3538
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 2560
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_qualification",schemaname="public"} 23689
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 24747
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 20228
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="serialized_dag",schemaname="public"} 483456
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="slot_pool",schemaname="public"} 26009
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_instance",schemaname="public"} 5.771058e+06
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_seq_tup_read{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_stat_user_tables_size_bytes Total disk space used by this table, in bytes, including all indexes and TOAST data
# TYPE pg_stat_user_tables_size_bytes gauge
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_group",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_group_role",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_permission",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_permission_view",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 73728
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_register_user",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_role",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_user",schemaname="public"} 81920
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_user_group",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_user_role",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="ab_view_menu",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="alembic_version",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_active",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_alias",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_event",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="asset_trigger",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="backfill",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="callback_request",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 114688
pg_stat_user_tables_size_bytes{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="competence",schemaname="public"} 1.10592e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="connection",schemaname="public"} 49152
pg_stat_user_tables_size_bytes{datname="francetravail",relname="contrat",schemaname="public"} 1.7235968e+07
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag",schemaname="public"} 98304
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_bundle",schemaname="public"} 57344
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_code",schemaname="public"} 999424
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_run",schemaname="public"} 262144
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_run_note",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_tag",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_version",schemaname="public"} 49152
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dag_warning",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="deadline",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="descriptionoffre",schemaname="public"} 1.62709504e+08
pg_stat_user_tables_size_bytes{datname="francetravail",relname="entreprise",schemaname="public"} 2.3666688e+07
pg_stat_user_tables_size_bytes{datname="francetravail",relname="experience",schemaname="public"} 221184
pg_stat_user_tables_size_bytes{datname="francetravail",relname="formation",schemaname="public"} 778240
pg_stat_user_tables_size_bytes{datname="francetravail",relname="import_error",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="job",schemaname="public"} 147456
pg_stat_user_tables_size_bytes{datname="francetravail",relname="langue",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="localisation",schemaname="public"} 1.1689984e+07
pg_stat_user_tables_size_bytes{datname="francetravail",relname="log",schemaname="public"} 81920
pg_stat_user_tables_size_bytes{datname="francetravail",relname="log_template",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_competence",schemaname="public"} 5.701632e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_experience",schemaname="public"} 6.610944e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_formation",schemaname="public"} 212992
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_langue",schemaname="public"} 368640
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 278528
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_qualification",schemaname="public"} 2.121728e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 2.29376e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="offreemploi",schemaname="public"} 7.110656e+06
pg_stat_user_tables_size_bytes{datname="francetravail",relname="permisconduire",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="qualification",schemaname="public"} 40960
pg_stat_user_tables_size_bytes{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 49152
pg_stat_user_tables_size_bytes{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 352256
pg_stat_user_tables_size_bytes{datname="francetravail",relname="serialized_dag",schemaname="public"} 589824
pg_stat_user_tables_size_bytes{datname="francetravail",relname="session",schemaname="public"} 57344
pg_stat_user_tables_size_bytes{datname="francetravail",relname="slot_pool",schemaname="public"} 49152
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_instance",schemaname="public"} 540672
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_instance_history",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_instance_note",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_map",schemaname="public"} 32768
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="task_reschedule",schemaname="public"} 8192
pg_stat_user_tables_size_bytes{datname="francetravail",relname="trigger",schemaname="public"} 16384
pg_stat_user_tables_size_bytes{datname="francetravail",relname="variable",schemaname="public"} 24576
pg_stat_user_tables_size_bytes{datname="francetravail",relname="xcom",schemaname="public"} 114688


# HELP pg_stat_user_tables_vacuum_count Number of times this table has been manually vacuumed (not counting VACUUM FULL)
# TYPE pg_stat_user_tables_vacuum_count counter
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="competence",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="connection",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="descriptionoffre",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="experience",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="formation",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="job",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="langue",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="log",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="session",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="variable",schemaname="public"} 0
pg_stat_user_tables_vacuum_count{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_static Version string as reported by postgres
# TYPE pg_static untyped
pg_static{server="postgres:5432",short_version="16.9.0",version="PostgreSQL 16.9 on x86_64-pc-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit"} 1


# HELP pg_statio_user_tables_heap_blocks_hit Number of buffer hits in this table
# TYPE pg_statio_user_tables_heap_blocks_hit counter
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_permission",schemaname="public"} 24770
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_permission_view",schemaname="public"} 6828
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 1858
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_role",schemaname="public"} 786
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_user",schemaname="public"} 193
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_user_role",schemaname="public"} 92
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="ab_view_menu",schemaname="public"} 25119
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="alembic_version",schemaname="public"} 18
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 3
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 9610
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="competence",schemaname="public"} 251355
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="connection",schemaname="public"} 22
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="contrat",schemaname="public"} 5.918535e+06
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag",schemaname="public"} 1.385171e+06
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_bundle",schemaname="public"} 20475
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_code",schemaname="public"} 6406
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_run",schemaname="public"} 686477
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_tag",schemaname="public"} 12783
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_version",schemaname="public"} 12622
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="descriptionoffre",schemaname="public"} 259585
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="entreprise",schemaname="public"} 172346
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="experience",schemaname="public"} 231452
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="formation",schemaname="public"} 11917
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="job",schemaname="public"} 146571
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="langue",schemaname="public"} 10677
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="localisation",schemaname="public"} 160852
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="log",schemaname="public"} 23
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="log_template",schemaname="public"} 24
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_competence",schemaname="public"} 305428
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_experience",schemaname="public"} 372185
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_formation",schemaname="public"} 9228
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_langue",schemaname="public"} 16984
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 12019
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_qualification",schemaname="public"} 115423
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 123399
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="offreemploi",schemaname="public"} 739271
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="permisconduire",schemaname="public"} 7715
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="qualification",schemaname="public"} 47395
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 74286
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 4577
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="serialized_dag",schemaname="public"} 13244
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="session",schemaname="public"} 161
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="slot_pool",schemaname="public"} 47893
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_instance",schemaname="public"} 1.021578e+06
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_map",schemaname="public"} 2362
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_hit{datname="francetravail",relname="xcom",schemaname="public"} 523


# HELP pg_statio_user_tables_heap_blocks_read Number of disk blocks read from this table
# TYPE pg_statio_user_tables_heap_blocks_read counter
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_permission",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_permission_view",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 4
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_role",schemaname="public"} 2
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_user",schemaname="public"} 2
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_user_role",schemaname="public"} 2
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="ab_view_menu",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 4
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="competence",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="connection",schemaname="public"} 3
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="contrat",schemaname="public"} 2911
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag",schemaname="public"} 5
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_bundle",schemaname="public"} 9
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_code",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="descriptionoffre",schemaname="public"} 29934
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="entreprise",schemaname="public"} 1459
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="experience",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="formation",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="job",schemaname="public"} 4
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="langue",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="localisation",schemaname="public"} 585
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="log",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="log_template",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_competence",schemaname="public"} 2
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_experience",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="offreemploi",schemaname="public"} 668
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 49
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="serialized_dag",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="session",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_instance",schemaname="public"} 4
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_map",schemaname="public"} 1
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_heap_blocks_read{datname="francetravail",relname="xcom",schemaname="public"} 1


# HELP pg_statio_user_tables_idx_blocks_hit Number of buffer hits in all indexes on this table
# TYPE pg_statio_user_tables_idx_blocks_hit counter
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_permission",schemaname="public"} 24749
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_permission_view",schemaname="public"} 3597
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 1137
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_role",schemaname="public"} 526
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_user",schemaname="public"} 348
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_user_role",schemaname="public"} 164
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="ab_view_menu",schemaname="public"} 19789
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="alembic_version",schemaname="public"} 19
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 4
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset",schemaname="public"} 107558
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_active",schemaname="public"} 648
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 43760
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_event",schemaname="public"} 444
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="asset_trigger",schemaname="public"} 212907
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="backfill",schemaname="public"} 22593
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 90425
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="callback_request",schemaname="public"} 105124
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 6654
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="competence",schemaname="public"} 272901
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="connection",schemaname="public"} 60
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="contrat",schemaname="public"} 355097
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag",schemaname="public"} 414860
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_bundle",schemaname="public"} 204
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_code",schemaname="public"} 110
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 19082
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 105125
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_run",schemaname="public"} 295867
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_run_note",schemaname="public"} 106
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 58804
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 7904
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 79786
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 7904
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_tag",schemaname="public"} 12844
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_version",schemaname="public"} 11233
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dag_warning",schemaname="public"} 235756
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 1101
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="descriptionoffre",schemaname="public"} 322201
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="entreprise",schemaname="public"} 310622
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="experience",schemaname="public"} 310220
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="formation",schemaname="public"} 21608
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="import_error",schemaname="public"} 16681
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="job",schemaname="public"} 64250
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="langue",schemaname="public"} 7177
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="localisation",schemaname="public"} 310615
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="log",schemaname="public"} 184
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="log_template",schemaname="public"} 39
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_competence",schemaname="public"} 243692
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_experience",schemaname="public"} 307239
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_formation",schemaname="public"} 7311
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_langue",schemaname="public"} 13646
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 9714
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_qualification",schemaname="public"} 94540
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 98959
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="offreemploi",schemaname="public"} 698109
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="permisconduire",schemaname="public"} 5179
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="qualification",schemaname="public"} 23721
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 49568
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 1285
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="serialized_dag",schemaname="public"} 1014
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="session",schemaname="public"} 125
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="slot_pool",schemaname="public"} 37
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_instance",schemaname="public"} 312159
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_instance_history",schemaname="public"} 14697
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_instance_note",schemaname="public"} 93
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_map",schemaname="public"} 2380
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 67060
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="task_reschedule",schemaname="public"} 221
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="trigger",schemaname="public"} 157112
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_hit{datname="francetravail",relname="xcom",schemaname="public"} 945


# HELP pg_statio_user_tables_idx_blocks_read Number of disk blocks read from all indexes on this table
# TYPE pg_statio_user_tables_idx_blocks_read counter
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_permission",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_permission_view",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_role",schemaname="public"} 7
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_user",schemaname="public"} 15
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_user_role",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="ab_view_menu",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="alembic_version",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_active",schemaname="public"} 6
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_event",schemaname="public"} 6
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="asset_trigger",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="backfill",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="callback_request",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 7
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="competence",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="connection",schemaname="public"} 13
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="contrat",schemaname="public"} 59
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag",schemaname="public"} 10
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_bundle",schemaname="public"} 4
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_code",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_run",schemaname="public"} 24
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_run_note",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_tag",schemaname="public"} 6
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_version",schemaname="public"} 7
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dag_warning",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 9
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="descriptionoffre",schemaname="public"} 41
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="entreprise",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="experience",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="formation",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="import_error",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="job",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="langue",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="localisation",schemaname="public"} 15
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="log",schemaname="public"} 4
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="log_template",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_competence",schemaname="public"} 22
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_experience",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_formation",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_langue",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_qualification",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="offreemploi",schemaname="public"} 292
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="permisconduire",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="qualification",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 9
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="serialized_dag",schemaname="public"} 8
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="session",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="slot_pool",schemaname="public"} 6
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_instance",schemaname="public"} 42
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_instance_history",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_instance_note",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_map",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 2
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="task_reschedule",schemaname="public"} 3
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="trigger",schemaname="public"} 1
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_idx_blocks_read{datname="francetravail",relname="xcom",schemaname="public"} 10


# HELP pg_statio_user_tables_tidx_blocks_hit Number of buffer hits in this table's TOAST table indexes (if any)
# TYPE pg_statio_user_tables_tidx_blocks_hit counter
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="competence",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="connection",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_code",schemaname="public"} 11751
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="descriptionoffre",schemaname="public"} 253558
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="experience",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="formation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="job",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="langue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="log",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="serialized_dag",schemaname="public"} 2671
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="session",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_hit{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_statio_user_tables_tidx_blocks_read Number of disk blocks read from this table's TOAST table indexes (if any)
# TYPE pg_statio_user_tables_tidx_blocks_read counter
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="competence",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="connection",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_code",schemaname="public"} 3
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="descriptionoffre",schemaname="public"} 67
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="experience",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="formation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="job",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="langue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="log",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="serialized_dag",schemaname="public"} 5
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="session",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_tidx_blocks_read{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_statio_user_tables_toast_blocks_hit Number of buffer hits in this table's TOAST table (if any)
# TYPE pg_statio_user_tables_toast_blocks_hit counter
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="competence",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="connection",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_code",schemaname="public"} 22244
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="descriptionoffre",schemaname="public"} 137174
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="experience",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="formation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="job",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="langue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="log",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="serialized_dag",schemaname="public"} 6374
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="session",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_hit{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_statio_user_tables_toast_blocks_read Number of disk blocks read from this table's TOAST table (if any)
# TYPE pg_statio_user_tables_toast_blocks_read counter
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_group",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_group_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_permission",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_permission_view",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_permission_view_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_register_user",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_user",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_user_group",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_user_role",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="ab_view_menu",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="alembic_version",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="alembic_version_fab",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_active",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_alias",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_alias_asset",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_alias_asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_dag_run_queue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="asset_trigger",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="backfill",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="backfill_dag_run",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="callback_request",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="celery_taskmeta",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="celery_tasksetmeta",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="competence",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="connection",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="contrat",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_bundle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_code",schemaname="public"} 5
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_owner_attributes",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_priority_parsing_request",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_run",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_run_note",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_schedule_asset_alias_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_schedule_asset_name_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_schedule_asset_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_schedule_asset_uri_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_tag",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_version",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dag_warning",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="dagrun_asset_event",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="deadline",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="descriptionoffre",schemaname="public"} 4112
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="entreprise",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="experience",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="formation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="import_error",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="job",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="langue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="localisation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="log",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="log_template",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_competence",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_experience",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_formation",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_langue",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_permisconduire",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_qualification",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offre_qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="offreemploi",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="permisconduire",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="qualification",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="qualiteprofessionnelle",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="rendered_task_instance_fields",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="serialized_dag",schemaname="public"} 116
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="session",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="slot_pool",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_instance",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_instance_history",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_instance_note",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_map",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_outlet_asset_reference",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="task_reschedule",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="trigger",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="variable",schemaname="public"} 0
pg_statio_user_tables_toast_blocks_read{datname="francetravail",relname="xcom",schemaname="public"} 0


# HELP pg_up Whether the last scrape of metrics from PostgreSQL was able to connect to the server (1 for yes, 0 for no).
# TYPE pg_up gauge
pg_up 1


# HELP pg_wal_segments Number of WAL segments
# TYPE pg_wal_segments gauge
pg_wal_segments 17


# HELP pg_wal_size_bytes Total size of WAL segments
# TYPE pg_wal_size_bytes gauge
pg_wal_size_bytes 2.85212672e+08


# HELP postgres_exporter_build_info A metric with a constant '1' value labeled by version, revision, branch, goversion from which postgres_exporter was built, and the goos and goarch for the build.
# TYPE postgres_exporter_build_info gauge
postgres_exporter_build_info{branch="HEAD",goarch="amd64",goos="linux",goversion="go1.23.6",revision="1e574cf4fd2a75a8a707d424eafcaa0b88cb7af4",tags="unknown",version="0.17.1"} 1


# HELP postgres_exporter_config_last_reload_success_timestamp_seconds Timestamp of the last successful configuration reload.
# TYPE postgres_exporter_config_last_reload_success_timestamp_seconds gauge
postgres_exporter_config_last_reload_success_timestamp_seconds 0


# HELP postgres_exporter_config_last_reload_successful Postgres exporter config loaded successfully.
# TYPE postgres_exporter_config_last_reload_successful gauge
postgres_exporter_config_last_reload_successful 0


# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 154.35


# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06


# HELP process_network_receive_bytes_total Number of bytes received by the process over the network.
# TYPE process_network_receive_bytes_total counter
process_network_receive_bytes_total 1.01643702e+08


# HELP process_network_transmit_bytes_total Number of bytes sent by the process over the network.
# TYPE process_network_transmit_bytes_total counter
process_network_transmit_bytes_total 4.9340863e+07


# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 14


# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.1364736e+07


# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.75191351263e+09


# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.268097024e+09


# HELP process_virtual_memory_max_bytes Maximum amount of virtual memory available in bytes.
# TYPE process_virtual_memory_max_bytes gauge
process_virtual_memory_max_bytes 1.8446744073709552e+19


# HELP promhttp_metric_handler_requests_in_flight Current number of scrapes being served.
# TYPE promhttp_metric_handler_requests_in_flight gauge
promhttp_metric_handler_requests_in_flight 1


# HELP promhttp_metric_handler_requests_total Total number of scrapes by HTTP status code.
# TYPE promhttp_metric_handler_requests_total counter
promhttp_metric_handler_requests_total{code="200"} 1446
promhttp_metric_handler_requests_total{code="500"} 0
promhttp_metric_handler_requests_total{code="503"} 0
