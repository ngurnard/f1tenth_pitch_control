import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


def animate_trajectory(car, control_v):
    """
    :param control_v: control input
    :param car: RaceCar object
    """
    # user input
    # try:
    #     u = float(input('Enter initial velocity (m/s): '))
    #     theta = float(input('Enter angle (deg): '))
    # except ValueError:
    #     print('Invalid input.')
    # else:
    #     theta = np.deg2rad(theta)

    u = car.take_off_v
    theta = car.angle0
    pitch_angles, _ = car.get_state_response(control_v)
    print([np.rad2deg(angle) for angle in pitch_angles])

    t = np.linspace(0, car.t_flight, len(pitch_angles))
    x = u * np.cos(theta) * t
    y = u * np.sin(theta) * t - 0.5 * car.g * t ** 2

    fig, ax = plt.subplots()
    line, = ax.plot(x, y, color='k')

    xmin = x[0]
    ymin = y[0]
    xmax = max(x)
    ymax = max(y)
    xysmall = min(xmax, ymax)
    maxscale = max(xmax, ymax)
    # circle = plt.Circle((xmin, ymin), radius=0.005)
    # ax.add_patch(circle)

    rect = patches.Rectangle((xmin, ymin), car.l, car.h, color="blue", rotation_point='center')
    ax.add_patch(rect)

    def update(num, x, y, line, rect, pitch_angles):
        line.set_data(x[:num], y[:num])
        # rect.center = x[num], y[num]
        center_x = x[num] - car.l / 2
        center_y = y[num] - car.h / 2
        tr = mpl.transforms.Affine2D().rotate_deg_around(x[num], y[num], pitch_angles[num] * 180/np.pi) \
                 .translate(x[num], y[num]) + ax.transData

        rect.set_transform(tr)
        line.axes.axis([0, max(np.append(x, y)), 0, max(np.append(x, y))])
        # line.axes.axis([0, max(np.append(center_x, center_y)), 0, max(np.append(center_x, center_y))])
        ax.set_xlim(min(x), 1.0)
        ax.set_ylim(min(y), 1.0)
        return line, rect

    ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line, rect, pitch_angles],
                                  interval=25, blit=True)

    plt.show()


def overlay_trajectory(car, control_v):
    _, traj = car.get_state_response(control_v)
    for i, s in enumerate(traj):
        x, y, pitch, t = s[:4]
        print(x, y, pitch, t)
        car_xmin = x - car.l / 2
        car_ymin = y - car.h / 2

        car_fig = mpl.patches.Rectangle(
            (car_xmin,
             car_ymin),
            car.l,
            car.h,
            rotation_point='center',
            alpha=(0.8 * i) / len(traj))
        rotation = mpl.transforms.Affine2D().rotate_deg_around(
            x, y, pitch * 180 / np.pi) + plt.gca().transData
        car_fig.set_transform(rotation)
        plt.gca().add_patch(car_fig)
    plt.title('Overlay car trajectory')
    plt.show()


def plot_pitch_angle(car):
    """
    Plot static pitch angle.
    :param car:
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    r1 = patches.Rectangle((0, 0), car.l, car.h, color="blue", alpha=0.50)
    r2 = patches.Rectangle((0, 0), car.l, car.h, color="red", alpha=0.50)
    t2 = mpl.transforms.Affine2D().rotate_deg(car.angle0 * 180) + ax.transData
    r2.set_transform(t2)
    ax.add_patch(r1)
    ax.add_patch(r2)
    plt.xlim(-1, 6)
    plt.ylim(-1, 6)
    plt.grid(True)
    plt.show()


def plot_projectile_motion(car, v):
    t = np.linspace(0, 5, num=100)  # Set time as 'continuous' parameter.
    x1 = []
    y1 = []
    for k in t:
        x = ((v * k) * np.cos(car.angle0))  # get positions at every point in time
        y = ((v * k) * np.sin(car.angle0)) - ((0.5 * car.g) * (k ** 2))
        x1.append(x)
        y1.append(y)
    p = [i for i, j in enumerate(y1) if j < 0]  # Don't fall through the floor
    for i in sorted(p, reverse=True):
        del x1[i]
        del y1[i]

    plt.plot(x1, y1)  # Plot for every angle
    plt.title('Parabola motion of car movement')
    plt.xlabel('x(t)')
    plt.ylabel('y(t)')
    plt.show()  # And show on one graphic