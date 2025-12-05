# ============================================================================
# PROJECT 3: AZURE TAG COMPLIANCE AUDITOR
# Problem: Ensure all resources have required tags for governance
# Topics: Dictionaries, Loops, Data Manipulation, Conditional Logic
# ============================================================================

import random

print("=" * 70)
print("🏷️  AZURE TAG COMPLIANCE AUDITOR")
print("=" * 70)

# ============================================================================
# DEFINE TAGGING POLICY
# ============================================================================

# Required tags for all resources
REQUIRED_TAGS = ["Environment", "CostCenter", "Owner", "Project"]

# Optional but recommended tags
RECOMMENDED_TAGS = ["DataClassification", "BackupPolicy", "MaintenanceWindow"]

# Valid values for certain tags
VALID_VALUES = {
    "Environment": ["Production", "Staging", "Development", "Test"],
    "DataClassification": ["Public", "Internal", "Confidential", "Restricted"],
    "BackupPolicy": ["Daily", "Weekly", "Monthly", "None"]
}

print("\n📋 Tagging Policy:")
print(f"  Required Tags: {', '.join(REQUIRED_TAGS)}")
print(f"  Recommended Tags: {', '.join(RECOMMENDED_TAGS)}")
print(f"  Total Tags Expected: {len(REQUIRED_TAGS) + len(RECOMMENDED_TAGS)}")

# ============================================================================
# GENERATE RESOURCE DATA
# ============================================================================

resource_types = ["Virtual Machine", "Storage Account", "SQL Database", "App Service", "Network Interface"]
possible_tags = {
    "Environment": ["Production", "Staging", "Development", "Test", ""],
    "CostCenter": ["IT-001", "HR-002", "Sales-003", "Marketing-004", ""],
    "Owner": ["john.doe@company.com", "jane.smith@company.com", "admin@company.com", ""],
    "Project": ["Project-Alpha", "Project-Beta", "Project-Gamma", ""],
    "DataClassification": ["Public", "Internal", "Confidential", "Restricted", ""],
    "BackupPolicy": ["Daily", "Weekly", "Monthly", "None", ""],
    "MaintenanceWindow": ["Weekend", "Weekday-Night", "Anytime", ""]
}

resources = []

for i in range(50):
    resource_type = random.choice(resource_types)
    
    # Generate random tags (some missing, some incorrect)
    tags = {}
    
    for tag_name, tag_values in possible_tags.items():
        # 70% chance of having each tag
        if random.random() < 0.7:
            value = random.choice(tag_values)
            if value:  # Not empty
                tags[tag_name] = value
    
    # Sometimes add invalid tags
    if random.random() < 0.1:
        tags["Department"] = random.choice(["Engineering", "Finance", "HR"])
    
    resource = {
        "name": f"{resource_type.lower().replace(' ', '-')}-{i+1:03d}",
        "type": resource_type,
        "resource_group": f"rg-{random.choice(['production', 'development', 'shared'])}",
        "location": random.choice(["East US", "West Europe", "Southeast Asia"]),
        "tags": tags
    }
    
    resources.append(resource)

print(f"\n✅ Auditing {len(resources)} Azure resources")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_required_tags(resource):
    """Check if resource has all required tags"""
    missing_tags = []
    for tag in REQUIRED_TAGS:
        if tag not in resource["tags"]:
            missing_tags.append(tag)
    return missing_tags

def check_recommended_tags(resource):
    """Check if resource has recommended tags"""
    missing_recommended = []
    for tag in RECOMMENDED_TAGS:
        if tag not in resource["tags"]:
            missing_recommended.append(tag)
    return missing_recommended

def validate_tag_values(resource):
    """Check if tag values are valid"""
    invalid_tags = []
    for tag_name, tag_value in resource["tags"].items():
        if tag_name in VALID_VALUES:
            if tag_value not in VALID_VALUES[tag_name]:
                invalid_tags.append({
                    "tag": tag_name,
                    "value": tag_value,
                    "valid_values": VALID_VALUES[tag_name]
                })
    return invalid_tags

def calculate_compliance_score(resource):
    """Calculate compliance score (0-100)"""
    score = 100
    
    # Required tags (50% of score)
    missing_required = check_required_tags(resource)
    score -= (len(missing_required) / len(REQUIRED_TAGS)) * 50
    
    # Recommended tags (30% of score)
    missing_recommended = check_recommended_tags(resource)
    score -= (len(missing_recommended) / len(RECOMMENDED_TAGS)) * 30
    
    # Valid values (20% of score)
    invalid_tags = validate_tag_values(resource)
    score -= len(invalid_tags) * 10
    
    return max(0, score)

# ============================================================================
# ANALYSIS 1: Overall Compliance
# ============================================================================
print("\n" + "=" * 70)
print("📊 OVERALL COMPLIANCE SUMMARY")
print("=" * 70)

compliant_resources = []
non_compliant_resources = []

for resource in resources:
    missing_required = check_required_tags(resource)
    if len(missing_required) == 0:
        compliant_resources.append(resource)
    else:
        non_compliant_resources.append(resource)

compliance_rate = (len(compliant_resources) / len(resources)) * 100

print(f"\n✅ Fully Compliant: {len(compliant_resources)} resources ({compliance_rate:.1f}%)")
print(f"❌ Non-Compliant: {len(non_compliant_resources)} resources ({100-compliance_rate:.1f}%)")

# Calculate average compliance score
avg_score = sum([calculate_compliance_score(r) for r in resources]) / len(resources)

print(f"\n📈 Average Compliance Score: {avg_score:.1f}/100")

if avg_score >= 90:
    print("   Status: 🟢 EXCELLENT")
elif avg_score >= 75:
    print("   Status: 🟡 GOOD")
elif avg_score >= 60:
    print("   Status: 🟠 NEEDS IMPROVEMENT")
else:
    print("   Status: 🔴 POOR - Immediate action required")

# ============================================================================
# ANALYSIS 2: Missing Required Tags
# ============================================================================
print("\n" + "=" * 70)
print("🔴 MISSING REQUIRED TAGS")
print("=" * 70)

# Count missing tags across all resources
missing_tag_counts = {tag: 0 for tag in REQUIRED_TAGS}

for resource in resources:
    missing = check_required_tags(resource)
    for tag in missing:
        missing_tag_counts[tag] += 1

print("\n📊 Missing Tag Statistics:")
for tag, count in sorted(missing_tag_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(resources)) * 100
    bar = "█" * int(pct / 2)
    print(f"  {tag:20s}: {count:3d} resources ({pct:5.1f}%) {bar}")

# Show resources with most missing tags
print("\n⚠️  Resources with Most Missing Tags:")
resources_by_missing = sorted(resources, 
                              key=lambda r: len(check_required_tags(r)), 
                              reverse=True)[:10]

for resource in resources_by_missing:
    missing = check_required_tags(resource)
    if missing:
        print(f"\n  🔴 {resource['name']}")
        print(f"     Type: {resource['type']}")
        print(f"     Missing: {', '.join(missing)}")

# ============================================================================
# ANALYSIS 3: Invalid Tag Values
# ============================================================================
print("\n" + "=" * 70)
print("⚠️  INVALID TAG VALUES")
print("=" * 70)

resources_with_invalid_tags = []

for resource in resources:
    invalid_tags = validate_tag_values(resource)
    if invalid_tags:
        resources_with_invalid_tags.append({
            "resource": resource,
            "invalid_tags": invalid_tags
        })

if resources_with_invalid_tags:
    print(f"\n⚠️  {len(resources_with_invalid_tags)} resource(s) with invalid tag values:\n")
    
    for item in resources_with_invalid_tags[:10]:
        resource = item["resource"]
        print(f"  ⚠️  {resource['name']}")
        for invalid in item["invalid_tags"]:
            print(f"     Tag: {invalid['tag']}")
            print(f"     Current Value: '{invalid['value']}'")
            print(f"     Valid Values: {', '.join(invalid['valid_values'])}")
        print()
else:
    print("\n✅ All tag values are valid")

# ============================================================================
# ANALYSIS 4: Missing Recommended Tags
# ============================================================================
print("=" * 70)
print("💡 RECOMMENDED TAGS ANALYSIS")
print("=" * 70)

# Count missing recommended tags
recommended_tag_counts = {tag: 0 for tag in RECOMMENDED_TAGS}

for resource in resources:
    missing_rec = check_recommended_tags(resource)
    for tag in missing_rec:
        recommended_tag_counts[tag] += 1

print("\n📊 Recommended Tag Coverage:")
for tag in RECOMMENDED_TAGS:
    missing_count = recommended_tag_counts[tag]
    present_count = len(resources) - missing_count
    coverage_pct = (present_count / len(resources)) * 100
    
    status = "✅" if coverage_pct >= 80 else "🟡" if coverage_pct >= 50 else "🔴"
    
    print(f"  {status} {tag:25s}: {present_count:3d}/{len(resources)} resources ({coverage_pct:5.1f}%)")

# ============================================================================
# ANALYSIS 5: Compliance by Resource Type
# ============================================================================
print("\n" + "=" * 70)
print("📊 COMPLIANCE BY RESOURCE TYPE")
print("=" * 70)

compliance_by_type = {}

for resource_type in resource_types:
    type_resources = [r for r in resources if r["type"] == resource_type]
    if type_resources:
        type_compliant = [r for r in type_resources if len(check_required_tags(r)) == 0]
        compliance_pct = (len(type_compliant) / len(type_resources)) * 100
        
        compliance_by_type[resource_type] = {
            "total": len(type_resources),
            "compliant": len(type_compliant),
            "compliance_pct": compliance_pct
        }

print(f"\n{'Resource Type':<25} {'Total':<8} {'Compliant':<12} {'Rate':<10}")
print("-" * 60)

for resource_type in sorted(compliance_by_type.keys(), 
                            key=lambda x: compliance_by_type[x]["compliance_pct"]):
    stats = compliance_by_type[resource_type]
    status = "✅" if stats["compliance_pct"] >= 90 else "🟡" if stats["compliance_pct"] >= 70 else "🔴"
    print(f"{resource_type:<25} {stats['total']:<8} {stats['compliant']:<12} {status} {stats['compliance_pct']:>5.1f}%")

# ============================================================================
# ANALYSIS 6: Tag Coverage Matrix
# ============================================================================
print("\n" + "=" * 70)
print("📋 TAG COVERAGE MATRIX")
print("=" * 70)

all_tags = REQUIRED_TAGS + RECOMMENDED_TAGS

# Count resources with each tag
tag_coverage = {}
for tag in all_tags:
    count = sum(1 for r in resources if tag in r["tags"])
    tag_coverage[tag] = count

print(f"\n{'Tag Name':<25} {'Coverage':<15} {'Status':<10}")
print("-" * 55)

for tag in all_tags:
    count = tag_coverage[tag]
    coverage_pct = (count / len(resources)) * 100
    is_required = tag in REQUIRED_TAGS
    
    if is_required:
        status = "✅ OK" if coverage_pct >= 95 else "🔴 CRITICAL" if coverage_pct < 80 else "🟡 WARNING"
        tag_label = f"{tag} [REQUIRED]"
    else:
        status = "✅ GOOD" if coverage_pct >= 80 else "🟡 LOW"
        tag_label = f"{tag} [OPTIONAL]"
    
    print(f"{tag_label:<25} {count}/{len(resources)} ({coverage_pct:>5.1f}%) {status}")

# ============================================================================
# GENERATE AUTO-REMEDIATION SCRIPT
# ============================================================================
print("\n" + "=" * 70)
print("🔧 AUTO-REMEDIATION SUGGESTIONS")
print("=" * 70)

remediation_commands = []

for resource in non_compliant_resources[:5]:  # Show first 5
    missing_tags = check_required_tags(resource)
    
    if missing_tags:
        print(f"\n📝 {resource['name']}:")
        print(f"   # Azure CLI commands to fix missing tags:")
        
        for tag in missing_tags:
            # Suggest default values
            default_value = ""
            if tag == "Environment":
                default_value = "Development"  # Safe default
            elif tag == "CostCenter":
                default_value = "UNASSIGNED"
            elif tag == "Owner":
                default_value = "ops-team@company.com"
            elif tag == "Project":
                default_value = "UNTAGGED"
            
            cmd = f"   az resource tag --tags {tag}='{default_value}' --ids {resource['name']}"
            print(cmd)
            remediation_commands.append(cmd)

if len(non_compliant_resources) > 5:
    print(f"\n   ... and {len(non_compliant_resources) - 5} more resources need attention")

# ============================================================================
# COMPLIANCE REPORT BY RESOURCE
# ============================================================================
print("\n" + "=" * 70)
print("📋 DETAILED COMPLIANCE REPORT")
print("=" * 70)

print(f"\n{'Resource Name':<30} {'Type':<20} {'Score':<8} {'Status':<12} {'Issues'}")
print("-" * 100)

for resource in sorted(resources, key=lambda r: calculate_compliance_score(r)):
    score = calculate_compliance_score(resource)
    missing = check_required_tags(resource)
    
    if score == 100:
        status = "✅ COMPLIANT"
        issues = "None"
    elif score >= 70:
        status = "🟡 PARTIAL"
        issues = f"{len(missing)} missing tags"
    else:
        status = "🔴 NON-COMPLIANT"
        issues = f"{len(missing)} missing tags"
    
    print(f"{resource['name']:<30} {resource['type']:<20} {score:>5.0f}/100  {status:<12} {issues}")

# ============================================================================
# FINAL RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 70)
print("💡 RECOMMENDATIONS & ACTION PLAN")
print("=" * 70)

print("\n🎯 Priority Actions:")

action_count = 1

# Action 1: Fix critical missing tags
if non_compliant_resources:
    print(f"\n{action_count}. [CRITICAL] Add required tags to {len(non_compliant_resources)} resources")
    print(f"   Impact: Enable proper cost allocation and governance")
    print(f"   Effort: ~{len(non_compliant_resources) * 2} minutes")
    action_count += 1

# Action 2: Fix invalid values
if resources_with_invalid_tags:
    print(f"\n{action_count}. [HIGH] Correct {len(resources_with_invalid_tags)} resources with invalid tag values")
    print(f"   Impact: Ensure data quality and reporting accuracy")
    action_count += 1

# Action 3: Add recommended tags
low_coverage_tags = [tag for tag, count in recommended_tag_counts.items() 
                     if (count / len(resources)) > 0.5]
if low_coverage_tags:
    print(f"\n{action_count}. [MEDIUM] Improve coverage for recommended tags: {', '.join(low_coverage_tags[:3])}")
    print(f"   Impact: Enhanced resource management and automation")
    action_count += 1

# Action 4: Implement automation
print(f"\n{action_count}. [MEDIUM] Implement Azure Policy to enforce tagging")
print(f"   Impact: Prevent future non-compliance")

print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)

print(f"""
Total Resources Audited: {len(resources)}
Fully Compliant: {len(compliant_resources)}
Non-Compliant: {len(non_compliant_resources)}
Average Compliance Score: {avg_score:.1f}/100

Most Missing Tag: {max(missing_tag_counts, key=missing_tag_counts.get)}
Resources Needing Attention: {len([r for r in resources if calculate_compliance_score(r) < 70])}

💡 Tip: Run 'az policy definition create' to enforce tagging policy
""")

print("=" * 70)
print("✅ Tag compliance audit complete!")
print("=" * 70)