MODULE Module1
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: Author
    !
    ! Version: 1.0
    !
    !***********************************************************

    VAR bool ready:=FALSE;
    VAR intnum job:=0;

    VAR robtarget target;

    !***********************************************************
    !
    ! Procedure main
    !
    !   This is the entry point of your program
    !
    !***********************************************************
    PROC main()
        WHILE TRUE DO
            WHILE ready=FALSE DO
                WaitTime 1;
            ENDWHILE

            IF job=1 THEN
                MoveJ target,v100,z30,tool0;
            ELSEIF job=2 THEN
                g_GripOut;
            ELSEIF job=3 THEN
                g_GripIn;
            ENDIF
        ENDWHILE
    ENDPROC
ENDMODULE
