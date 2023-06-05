MODULE Module1
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: abina
    !
    ! Version: 1.0
    !
    !***********************************************************

    VAR bool ready := FALSE;
    VAR robtarget target;

    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PROC main()
        WHILE ready = FALSE DO
            WaitTime 1;
        ENDWHILE

        MoveL target, v100, z30, tool0;
    ENDPROC
ENDMODULE
