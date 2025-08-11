#!/usr/bin/env python3
"""
Workout Video Organizer
This script reorganizes workout videos by separating male and female workout videos 
into dedicated folder structures while maintaining category organization.
"""

import os
import shutil
from pathlib import Path

def organize_workout_videos():
    # Base workout directory
    base_dir = Path(r"C:\Users\rafic\Desktop\WorkOuts")
    
    # List of workout categories to organize
    workout_categories = [
        "3D Fitness Reels Format",
        "Arms Workout", 
        "Back Workout",
        "Biceps Workout",
        "Body Workout",
        "Calves Workout", 
        "Cardio Workout",
        "Chest Workout",
        "Dumbbell Workout",
        "Forearms Workout",
        "Hamstrings Workout",
        "Hips Workout",
        "Jumping Workout",
        "Leg Workout",
        "Neck Workout",
        "Quadriceps Workout", 
        "Random Workout",
        "Shoulders Workout",
        "Squat Workout",
        "Triceps Workout",
        "Waist Workout"
    ]
    
    # Create main Male and Female workout directories
    male_dir = base_dir / "Male Workout"
    female_dir = base_dir / "Female Workout"
    
    male_dir.mkdir(exist_ok=True)
    female_dir.mkdir(exist_ok=True)
    
    print("🏋️ Workout Video Organizer Started")
    print("=" * 50)
    
    # Create subdirectories in Male and Female workout folders
    print("📁 Creating category subdirectories...")
    for category in workout_categories:
        male_subdir = male_dir / category
        female_subdir = female_dir / category
        
        male_subdir.mkdir(exist_ok=True)
        female_subdir.mkdir(exist_ok=True)
        print(f"   ✓ Created: {category}")
    
    print("\n🔄 Moving workout videos...")
    
    # Statistics tracking
    stats = {
        'total_files': 0,
        'male_files': 0,
        'female_files': 0,
        'unspecified_files': 0,
        'moved_files': 0,
        'errors': 0
    }
    
    # Process each category
    for category in workout_categories:
        source_dir = base_dir / category
        
        if source_dir.exists() and source_dir.is_dir():
            print(f"\n📂 Processing: {category}")
            
            # Get all video files in the category
            video_files = list(source_dir.glob("*.mp4"))
            
            for video_file in video_files:
                stats['total_files'] += 1
                filename = video_file.name.lower()
                
                try:
                    # Determine destination based on filename content
                    if "(female)" in filename or "-female" in filename:
                        dest_dir = female_dir / category
                        dest_file = dest_dir / video_file.name
                        stats['female_files'] += 1
                        gender_label = "👩 FEMALE"
                        
                    elif "(male)" in filename or "-male" in filename:
                        dest_dir = male_dir / category
                        dest_file = dest_dir / video_file.name
                        stats['male_files'] += 1
                        gender_label = "👨 MALE"
                        
                    else:
                        # Files without clear gender designation - move to male by default
                        dest_dir = male_dir / category
                        dest_file = dest_dir / video_file.name
                        stats['unspecified_files'] += 1
                        gender_label = "❓ UNSPECIFIED (→ Male)"
                    
                    # Move the file
                    shutil.move(str(video_file), str(dest_file))
                    stats['moved_files'] += 1
                    
                    # Display progress (truncate long filenames)
                    display_name = video_file.name[:60] + "..." if len(video_file.name) > 60 else video_file.name
                    print(f"   {gender_label}: {display_name}")
                    
                except Exception as e:
                    stats['errors'] += 1
                    print(f"   ❌ ERROR moving {video_file.name}: {e}")
    
    print("\n🧹 Cleaning up empty directories...")
    empty_dirs_removed = 0
    
    for category in workout_categories:
        source_dir = base_dir / category
        if source_dir.exists():
            try:
                # Check if directory is empty
                if not any(source_dir.iterdir()):
                    source_dir.rmdir()
                    empty_dirs_removed += 1
                    print(f"   ✓ Removed empty: {category}")
                else:
                    remaining_items = list(source_dir.iterdir())
                    print(f"   ⚠️  {category} still contains {len(remaining_items)} items")
            except Exception as e:
                print(f"   ❌ Could not remove {category}: {e}")
    
    # Final statistics
    print("\n" + "=" * 50)
    print("📊 ORGANIZATION SUMMARY")
    print("=" * 50)
    print(f"Total video files processed: {stats['total_files']}")
    print(f"Male workout videos: {stats['male_files']}")
    print(f"Female workout videos: {stats['female_files']}")
    print(f"Unspecified videos (moved to Male): {stats['unspecified_files']}")
    print(f"Successfully moved files: {stats['moved_files']}")
    print(f"Empty directories cleaned: {empty_dirs_removed}")
    
    if stats['errors'] > 0:
        print(f"⚠️  Errors encountered: {stats['errors']}")
    
    print("\n✅ Workout video organization completed!")
    print("\n📁 New structure:")
    print("   📂 Male Workout/")
    print("      └── [All workout categories with male videos]")
    print("   📂 Female Workout/")
    print("      └── [All workout categories with female videos]")

def verify_organization():
    """Verify the organization was successful"""
    base_dir = Path(r"C:\Users\rafic\Desktop\WorkOuts")
    male_dir = base_dir / "Male Workout"
    female_dir = base_dir / "Female Workout"
    
    print("\n🔍 VERIFICATION REPORT")
    print("=" * 30)
    
    if male_dir.exists():
        male_categories = [d.name for d in male_dir.iterdir() if d.is_dir()]
        male_video_count = sum(len(list((male_dir / cat).glob("*.mp4"))) for cat in male_categories)
        print(f"👨 Male Workout: {len(male_categories)} categories, {male_video_count} videos")
    
    if female_dir.exists():
        female_categories = [d.name for d in female_dir.iterdir() if d.is_dir()]
        female_video_count = sum(len(list((female_dir / cat).glob("*.mp4"))) for cat in female_categories)
        print(f"👩 Female Workout: {len(female_categories)} categories, {female_video_count} videos")

if __name__ == "__main__":
    try:
        organize_workout_videos()
        verify_organization()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the paths and try again.")