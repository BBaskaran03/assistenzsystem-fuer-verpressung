MODULE Module2
    !***********************************************************
    !
    ! Module:  Module2
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

    VAR robtarget currentPos;
    VAR intnum move_by_x;
    VAR intnum move_by_y;
    VAR intnum move_by_z;

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
                ! g_GripOut;
            ELSEIF job=3 THEN
                ! g_GripIn;
            ELSEIF job=4 THEN
                MoveL RelTool (currentPos, move_by_x, move_by_y, move_by_z), v100, fine, tool0;
            ENDIF
        ENDWHILE
    ENDPROC
ENDMODULE
