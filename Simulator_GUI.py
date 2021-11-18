from typing import Text
import PySimpleGUI as sg
import os
import math
import cv2

def speckle_image(values):

    vals = ['SPECKLE','PX_WIDTH','PX_HEIGHT','BASE_NAME']
    any_field = 0
    for val in vals:
        if values[val] == '':
            window[val].update(background_color='#db000d')
            any_field = 1
        else:
            window[val].update(background_color='white')
    
    if any_field:
        sg.popup(f'Missing fields.')
        return
    
    img = values['SPECKLE']
    res_px = [int(values['PX_WIDTH']),int(values['PX_HEIGHT'])]
    ref_img = cv2.imread(img,0)

    new_img = ref_img[0:res_px[1],0:res_px[0]]

    base = values['BASE_NAME']
    cv2.imwrite(f'{base}_speckle.bmp',new_img)

    os.popen(f'{base}_speckle.bmp')

def calibration_file(values):

    vals = ['FX_0','FY_0','FS_0','K1_0','K2_0','K3_0','P1_0','P2_0','CX_0','CY_0','FX_1','FY_1','FS_1','K1_1','K2_1','K3_1','P1_1','P2_1','CX_1','CY_1','TX','TY','TZ','THETA','PHI','PSI','BASE_NAME']
    any_field = 0
    for val in vals:
        if values[val] == '':
            window[val].update(background_color='#db000d')
            any_field = 1
        else:
            window[val].update(background_color='white')
        
    if any_field:
        sg.popup(f'Missing fields.')
        return
    Fx_0 = float(values['FX_0'])
    Fx_1 = float(values['FX_1'])
    Fy_0 = float(values['FY_0'])
    Fy_1 = float(values['FY_1'])
    Fs_0 = float(values['FS_0'])
    Fs_1 = float(values['FS_1'])
    K1_0 = float(values['K1_0'])
    K1_1 = float(values['K1_1'])
    K2_0 = float(values['K2_0'])
    K2_1 = float(values['K2_1'])
    K3_0 = float(values['K3_0'])
    K3_1 = float(values['K3_1'])
    P1_0 = float(values['P1_0'])
    P1_1 = float(values['P1_1'])
    P2_0 = float(values['P2_0'])
    P2_1 = float(values['P2_1'])
    Cx_0 = float(values['CX_0'])
    Cx_1 = float(values['CX_1'])
    Cy_0 = float(values['CY_0'])
    Cy_1 = float(values['CY_1'])
    Tx = float(values['TX'])
    Ty = float(values['TY'])
    Tz = float(values['TZ'])
    Theta = float(values['THETA'])
    Phi = float(values['PHI'])
    Psi = float(values['PSI'])

    cal_data = [
        f'Cam0_Fx [pixels];{Fx_0:.2f}',
        f'Cam0_Fy [pixels];{Fy_0:.2f}',
        f'Cam0_Fs [pixels];{Fs_0:.2f}',
        f'Cam0_Kappa 1;{K1_0:.2f}',
        f'Cam0_Kappa 2;{K2_0:.2f}',
        f'Cam0_Kappa 3;{K3_0:.2f}',
        f'Cam0_P1;{P1_0:.2f}',
        f'Cam0_P2;{P2_0:.2f}',
        f'Cam0_Cx [pixels];{Cx_0:.2f}',
        f'Cam0_Cy [pixels];{Cy_0:.2f}',

        f'Cam1_Fx [pixels];{Fx_1:.2f}',
        f'Cam1_Fy [pixels];{Fy_1:.2f}',
        f'Cam1_Fs [pixels];{Fs_1:.2f}',
        f'Cam1_Kappa 1;{K1_1:.2f}',
        f'Cam1_Kappa 2;{K2_1:.2f}',
        f'Cam1_Kappa 3;{K3_1:.2f}',
        f'Cam1_P1;{P1_1:.2f}',
        f'Cam1_P2;{P2_1:.2f}',
        f'Cam1_Cx [pixels];{Cx_1:.2f}',
        f'Cam1_Cy [pixels];{Cy_1:.2f}',

        f'Tx [mm];{Tx:.2f}',
        f'Ty [mm];{Ty:.2f}',
        f'Tz [mm];{Tz:.2f}',
        f'Theta [deg];{Theta:.2f}',
        f'Phi [deg];{Phi:.2f}',
        f'Psi [deg];{Psi:.2f}',
    ]

    cal_data = [f'{line}\n' for line in cal_data]

    base = values['BASE_NAME']
    with open(f'{base}.caldat','w') as file:
        for line in cal_data: file.write(line)

    os.popen(f'{base}.caldat')


def camera_calibration(values):

    fov = [float(values['WIDTH']),float(values['HEIGHT'])]
    res_px = [float(values['PX_WIDTH']),float(values['PX_HEIGHT'])]
    res_mm = [float(values['MM_WIDTH']),float(values['MM_HEIGHT'])]
    f = float(values['FOCAL_LENGTH'])
    theta = float(values['THETA'])
    # phi = float(values['PHI'])

    So = max(fov)*f/max(res_mm)
    Fx = round(f/(res_mm[0]/res_px[0]))
    Fy = round(f/(res_mm[0]/res_px[0]))
    Cx = round(res_px[0]/2)
    Cy = round(res_px[1]/2)

    # Tx = So*math.sin(math.radians(phi))
    # Tz = So*(1 - math.cos(math.radians(phi)))

    Ty = So*math.sin(math.radians(theta))
    Tz = So*(1 - math.cos(math.radians(theta)))

    return round(So),Fx,Fy,Cx,Cy,round(Ty),round(Tz)

debug = open('debug.txt','w')
print = sg.Print

browse_layout = [
    [
        sg.Text("Select Image"),
        sg.In(size=(62,1),enable_events=True,key="SPECKLE"),
        sg.FileBrowse(),
    ]
]

browse = [[sg.Frame('Speckle Pattern',browse_layout)]]

fov_layout = [   
    [
        sg.Text('Width',size=(5,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='WIDTH')
    ],
    [
        sg.Text('Height',size=(5,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='HEIGHT')
    ],
]

fov = [[sg.Frame('Field-of-View',fov_layout)]]

lenses_layout = [   
    [
        sg.Text('Focal Length',size=(15,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='FOCAL_LENGTH')
    ],
    [
        sg.Text('Minimum Distance',size=(15,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='MINIMUM_DISTANCE')
    ],
    [
        sg.Text('Estimated Distance',size=(15,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',justification='center',size=(8,10),visible=False,key='ESTIMATED_DISTANCE')
    ],
]

lenses = [[sg.Frame('Lenses',lenses_layout)]]

camera_layout = [   
    [
        sg.Text('',size=(8,1),justification='right'),
        sg.Text('Width',justification='center',size=(7,1)),
        sg.Text('Heigth',justification='center',size=(7,1)),
    ],
    [
        sg.Text('Pixels',size=(8,1),justification='right'),
        sg.Input('',tooltip='Units: pixel',enable_events=True,justification='center',size=(8,10),key='PX_WIDTH'),
        sg.Input('',tooltip='Units: pixel',enable_events=True,justification='center',size=(8,10),key='PX_HEIGHT')
    ],
    [
        sg.Text('Milimeters',size=(8,1),justification='right'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='MM_WIDTH'),
        sg.Input('',tooltip='Units: milimeters',enable_events=True,justification='center',size=(8,10),key='MM_HEIGHT')
    ],
]

camera = [[sg.Frame('Camera Resolution',camera_layout)]]

camera_layout = [   
    [
        sg.Text('',size=(2,1),justification='right'),
        sg.Text('Cam 0',justification='center',size=(7,1)),
        sg.Text('Cam 1',justification='center',size=(7,1)),
    ],
    [
        sg.Text('Fx',size=(2,1),justification='right',           tooltip='Focal length in x-direction (pixels)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FX_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FX_1')
    ],
    [
        sg.Text('Fy',size=(2,1),justification='right',           tooltip='Focal length in y-direction (pixels)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FY_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FY_1')
    ],
    [
        sg.Text('Fs',size=(2,1),justification='right',           tooltip='Skewing'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FS_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='FS_1')
    ],
    [
        sg.Text('K1',size=(2,1),justification='right',           tooltip='Radial distortion of 1st order'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K1_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K1_1')
    ],
    [
        sg.Text('K2',size=(2,1),justification='right',           tooltip='Radial distortion of 2nd order'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K2_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K2_1')
    ],
    [
        sg.Text('K3',size=(2,1),justification='right',           tooltip='Radial distortion of 3rd order'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K3_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='K3_1')
    ],
    [
        sg.Text('P1',size=(2,1),justification='right',           tooltip='Tangential distortion 1st parameter'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='P1_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='P1_1')
    ],
    [
        sg.Text('P2',size=(2,1),justification='right',           tooltip='Tangential distortion 2nd parameter'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='P2_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='P2_1')
    ],
    [
        sg.Text('Cx',size=(2,1),justification='right',           tooltip='Principal point in x-direction (pixels)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='CX_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='CX_1')
    ],
    [
        sg.Text('Cy',size=(2,1),justification='right',           tooltip='Principal point in y-direction (pixels)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='CY_0'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='CY_1')
    ],
]

extrinsic_layout = [   
    [
        sg.Text('',size=(4,1),justification='right'),
        sg.Text('Extrinsic',justification='center',size=(7,1)),
    ],
    [
        sg.Text('Tx',size=(4,1),justification='right',                tooltip='Camera distance in x-direction (milimeters)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='TX'),
    ],
    [
        sg.Text('Ty',size=(4,1),justification='right',                tooltip='Camera distance in y-direction (milimeters)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='TY'),
    ],
    [
        sg.Text('Tz',size=(4,1),justification='right',           tooltip='Camera distance in z-direction (milimeters)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='TZ'),
    ],
    [
        sg.Text('Theta',size=(4,1),justification='right',           tooltip='Stereo-angle around x-axis (degrees)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='THETA'),
    ],
    [
        sg.Text('Phi',size=(4,1),justification='right',           tooltip='Stereo-angle around y-axis (degrees)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='PHI'),
    ],
        [
        sg.Text('Psi',size=(4,1),justification='right',           tooltip='Stereo-angle around z-axis (degrees)'),
        sg.Input('',enable_events=True,justification='center',size=(8,10),key='PSI'),
    ],
    [
        sg.Button('Clear',size=(8,1),pad=((20,0),(25,10)),tooltip='Clear camera calibration settings',key='CAL_CLEAR'),
    ],
    [
        sg.Button('Calculate',size=(8,1),pad=((20,0),(0,0)),tooltip='Compute Fx, Fy, Cx, Cy, and Ty based on stereo-angle, camera and lenses settings',key='CALCULATE'),
    ],
]
calibration_layout = [
    [
        sg.Column(camera_layout,vertical_alignment='top'),
        sg.Column(extrinsic_layout,vertical_alignment='top'),
        
    ], 
]
calibration = [[sg.Frame('Calibration Parameters',calibration_layout)]]

base_layout = [
    [
        sg.Text("Base Name"),
        sg.Input(size=(25,1),enable_events=True,key="BASE_NAME"),
    ]
]

buttons = [
    [
        sg.Frame('',base_layout,pad=((0,0),(11,40)))
    ],

    [
        sg.Button('Dummy',size=(6,1),pad=((80,0),(0,40)),tooltip='Set dummy parameters',key='DUMMY'),
        sg.Button('Clear',size=(6,1),pad=((16,0),(0,40)),tooltip='Clear all fields',key='CLEAR'),
    ],
    [
        sg.Button('Speckle Image',size=(15,1),pad=((80,0),(0,5)),tooltip='Generate speckle pattern image with camera resolution',key='IMAGE'),
    ],
    [
        sg.Button('Calibration File',size=(15,1),pad=((80,0),(5,0)),tooltip='Generate calibration file',key='CAL_FILE'),
    ],
    [
        sg.Button('Launch MatchID',size=(15,1),pad=((80,0),(40,0)),tooltip='Launch MatchID Stereo',key='MATCHID'),
    ]
]
# ----- Full layout -----
layout = [
    [
        browse,
        [
            sg.Column(fov,vertical_alignment='top'),
            sg.Column(lenses,vertical_alignment='top'),
            sg.Column(camera,vertical_alignment='top'),
        ],
        sg.Column(calibration,vertical_alignment='top'),
        sg.Column(buttons,vertical_alignment='top')
    ]
]

window = sg.Window("Stereo-DIC Simulator", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == 'SPECKLE':
        if not values[event].endswith(('.bmp','.tiff')):
            sg.popup('File format invalid: should be one of "bmp" or "tiff"')
            window['SPECKLE'].update('')

    elif event == 'CLEAR':
        blank = ['BASE_NAME','SPECKLE','WIDTH','HEIGHT','FOCAL_LENGTH','MINIMUM_DISTANCE','ESTIMATED_DISTANCE','PX_WIDTH','PX_HEIGHT','MM_WIDTH','MM_HEIGHT','THETA','FX_0','FY_0','FS_0','K1_0','K2_0','K3_0','P1_0','P2_0','CX_0','CY_0','FX_1','FY_1','FS_1','K1_1','K2_1','K3_1','P1_1','P2_1','CX_1','CY_1','TX','TY','TZ','THETA','PHI','PSI']

        for val in blank: window[val].update('',background_color='white')
        window['ESTIMATED_DISTANCE'].update(visible=False)

    elif event == 'DUMMY':
        dummy = {'WIDTH': 76,'HEIGHT': 96,'FOCAL_LENGTH': 50, 'MINIMUM_DISTANCE': 450,'PX_WIDTH': 1392,'PX_HEIGHT': 1040, 'MM_WIDTH': 8.8,'MM_HEIGHT': 6.4,'THETA': 20 }

        for val in dummy.keys(): window[val].update(dummy[val])

    elif event == 'CAL_CLEAR':
        blank = ['FX_0','FY_0','FS_0','K1_0','K2_0','K3_0','P1_0','P2_0','CX_0','CY_0','FX_1','FY_1','FS_1','K1_1','K2_1','K3_1','P1_1','P2_1','CX_1','CY_1','TX','TY','TZ','THETA','PHI','PSI']
        
        for val in blank: window[val].update('',background_color='white')
        window['ESTIMATED_DISTANCE'].update('',visible=False)

    elif event == 'CALCULATE':
        vals = ['WIDTH','HEIGHT','PX_WIDTH','PX_HEIGHT','MM_WIDTH','MM_HEIGHT','FOCAL_LENGTH','THETA']

        any_field = 0
        for val in vals:
            if values[val] == '':
                window[val].update(background_color='#db000d')
                any_field = 1
            else:
                window[val].update(background_color='white')
        
        if any_field:
            sg.popup(f'Missing fields.')
        else:
            # So,Fx,Fy,Cx,Cy,Ty = camera_calibration(values)
            # So,Fx,Fy,Cx,Cy,Tx,Tz = camera_calibration(values)
            So,Fx,Fy,Cx,Cy,Ty,Tz = camera_calibration(values)

            for val in ['FX_0','FX_1']: window[val].update(Fx)
            for val in ['FY_0','FY_1']: window[val].update(Fy)
            for val in ['CX_0','CX_1']: window[val].update(Cx)
            for val in ['CY_0','CY_1']: window[val].update(Cy)
            window['TY'].update(Ty)
            # window['TX'].update(Tx)
            window['TZ'].update(Tz)

            blank = ['FS_0','K1_0','K2_0','K3_0','P1_0','P2_0','FS_1','K1_1','K2_1','K3_1','P1_1','P2_1','TX','PHI','PSI']
            for val in blank: window[val].update('0')
            minS = values['MINIMUM_DISTANCE']
            thresh = 0
            if minS != '':
                if So >= float(minS):
                    window['ESTIMATED_DISTANCE'].update(So,background_color='lime',visible=True)
                else:
                    window['ESTIMATED_DISTANCE'].update(So,background_color='#db000d',visible=True)
            else:
                window['ESTIMATED_DISTANCE'].update(So,visible=True)

    elif event == 'CAL_FILE':
        calibration_file(values)

    elif event == 'IMAGE':
        speckle_image(values)

    elif event == 'MATCHID':
        try:
            os.popen('matchidstereo')
        except:
            pass

window.close()