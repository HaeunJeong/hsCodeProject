from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models import MappingRule, Product

class MappingRuleService:
    @staticmethod
    async def create_rule(
        db: Session,
        name: str,
        category: str,
        conditionField: str,
        conditionType: str,
        conditionValue: str,
        hsCode: str,
        priority: int = 0
    ) -> MappingRule:
        """새로운 매핑 룰을 생성합니다."""
        rule = MappingRule(
            name=name,
            category=category,
            conditionField=conditionField,
            conditionType=conditionType,
            conditionValue=conditionValue,
            hsCode=hsCode,
            priority=priority
        )
        db.add(rule)
        await db.commit()
        await db.refresh(rule)
        return rule

    @staticmethod
    async def get_rules(
        db: Session,
        category: Optional[str] = None,
        isActive: Optional[bool] = None
    ) -> List[MappingRule]:
        """매핑 룰 목록을 조회합니다."""
        query = db.query(MappingRule)
        if category:
            query = query.filter(MappingRule.category == category)
        if isActive is not None:
            query = query.filter(MappingRule.isActive == isActive)
        return await query.order_by(MappingRule.priority.desc()).all()

    @staticmethod
    async def update_rule(
        db: Session,
        rule_id: int,
        **kwargs
    ) -> Optional[MappingRule]:
        """매핑 룰을 업데이트합니다."""
        rule = await db.query(MappingRule).filter(MappingRule.id == rule_id).first()
        if not rule:
            return None

        for key, value in kwargs.items():
            setattr(rule, key, value)

        await db.commit()
        await db.refresh(rule)
        return rule

    @staticmethod
    async def delete_rule(
        db: Session,
        rule_id: int
    ) -> bool:
        """매핑 룰을 삭제합니다."""
        rule = await db.query(MappingRule).filter(MappingRule.id == rule_id).first()
        if not rule:
            return False

        await db.delete(rule)
        await db.commit()
        return True

    @staticmethod
    async def apply_rules(
        db: Session,
        product: Dict[str, Any],
        category: Optional[str] = None
    ) -> Optional[str]:
        """제품에 매핑 룰을 적용하여 HS 코드를 결정합니다."""
        rules = await MappingRuleService.get_rules(db, category, isActive=True)
        
        for rule in rules:
            field_value = product.get(rule.conditionField)
            if not field_value:
                continue

            if rule.conditionType == 'contains':
                if rule.conditionValue.lower() in str(field_value).lower():
                    return rule.hsCode
            elif rule.conditionType == 'equals':
                if str(field_value).lower() == rule.conditionValue.lower():
                    return rule.hsCode
            elif rule.conditionType == 'startswith':
                if str(field_value).lower().startswith(rule.conditionValue.lower()):
                    return rule.hsCode

        return None 