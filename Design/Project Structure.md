framework/
    core/
        task.py
        task_context.py
        task_state.py
        task_executor.py
        task_repository.py
        task_registry.py

    runtime/
        qt_executor.py
        cli_executor.py

    adapters/
        qt/
            qt_context.py
        cli/
            cli_context.py

domain/
    tasks/
        demo_task.py

ui/
    presenters/
        base_presenter.py
        demo_presenter.py
    views/
        demo_view.py

app/
    main_qt.py
    main_cli.py
    main_entry.py