function circleCollidesWithRectangle({
    circle,
    rectangle,
    boundary
}) {

    const padding = boundary.width / 2 - circle.radius - 1

    return circle.position.y - circle.radius + circle.velocity.y <= rectangle.position.y + rectangle.height + padding &&
        circle.position.x - circle.radius + circle.velocity.x <= rectangle.position.x + rectangle.width + padding &&
        circle.position.x + circle.radius + circle.velocity.x >= rectangle.position.x - padding &&
        circle.position.y + circle.radius + circle.velocity.y >= rectangle.position.y - padding;

}

function circleCollidesWithCircle({
    first,
    second
}) {
    return Math.hypot(
        first.position.x - second.position.x,
        first.position.y - second.position.y

    ) < first.radius + second.radius

}

function circleCollidesWithPoint({
    circle,
    point
}) {

    // console.log(
    //     (circle.position.x - point.x) * (circle.position.x - point.x)
    // )
    // console.log(
    //     (circle.position.y - point.y) * (circle.position.y - point.y)
    // )
    // console.log(
    //     (circle.radius) * (circle.radius)
    // )

    return (
        (circle.position.x - point.x) * (circle.position.x - point.x) +
        (circle.position.y - point.y) * (circle.position.y - point.y) <
        (circle.radius) * (circle.radius)
    )
}

export {
    circleCollidesWithRectangle,
    circleCollidesWithCircle,
    circleCollidesWithPoint
}