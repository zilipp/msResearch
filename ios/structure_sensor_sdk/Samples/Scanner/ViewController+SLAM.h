/*
  This file is part of the Structure SDK.
  Copyright © 2019 Occipital, Inc. All rights reserved.
  http://structure.io
*/

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>

#import "ViewController.h"
#import <Structure/Structure.h>

#import "MeshViewController.h"

@interface ViewController (SLAM)

- (void)setupSLAM;
- (void)resetSLAM;
- (void)clearSLAM;
- (void)setupMapper;
- (void)processDepthFrame:(STDepthFrame *)depthFrame
          colorFrameOrNil:(STColorFrame *)colorFrame;

@end
