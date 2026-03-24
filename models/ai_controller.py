from models.paddle import Paddle
from models.ball import Ball


class AIController:

    def update(self, paddle: Paddle, ball: Ball) -> None:
        paddle_center = paddle.y + paddle.height // 2
        if paddle_center < ball.y:
            paddle.move_down()
        elif paddle_center > ball.y:
            paddle.move_up()